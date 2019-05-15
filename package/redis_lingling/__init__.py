#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import redis
import threading
import time
from redis_lingling.mysql_lingling import MySQLTool
from redis_lingling.key import Key

# 和redis交互示例
# host是redis主机，需要启动 ./redis-server
# redis默认port（端口）是6379
# decode_responses=True，写入的键值对中的value为str类型，不加这个参数写入的则为字节类型
# password 需要密码。非同机访问，需要填写密码才可以访问
# r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
# # key是"foo" value是"bar" 将键值对存入redis缓存
# r.set('foo', 'is foo')
# # 取出键foo对应的值，这两种方式都可以
# print(r['foo'])
# print(r.get('foo'))


"""
KeyValueGetter: key-value获取控制器
功能说明：
【请求池】：
1、用户注册的key，将被添加进请求池之中；
2、请求池里的key，会不断判断是否过期，过期后则去Redis或Redis获取最新的值；
3、过期后触发请求，但获取值仍然正常获取原先的默认值，只有请求成功后，才会更新原先的默认值（确保实时性）；
4、过期后，先从Redis获取；无法从Redis获取时，从MySQL获取，并更新到Redis里；
【key】：
1、只有用户注册的key，才有效，否则返回空字符串；
2、维持一个请求池，请求池里的内容将定期从Redis或MySQL里获取；
3、本机缓存每个注册的key，默认过期时间是5000ms；
"""


def log(msg):
    # with open('./error.log', 'wa')as f:
    #     f.write(msg)
    print(msg)


class KeyValueGetter(object):

    # 初始化函数，常见初始配置是
    # host='localhost',
    # port=6379,
    # decode_responses=True,
    # password=''
    def __init__(self, redis_args, mysql_args):
        self._redis_args = redis_args
        self._mysql_args = mysql_args
        self.kv_pool = {}

        t1 = threading.Thread(target=self._eventloop, name='loop')
        t1.start()
        print('__init__ end')

    # 注册监听一个key
    # key: key值，必须是string类型
    # default_val: 默认值，必须是string类型，必须设置
    # expire_time：过期时间，默认值为5000（单位ms）
    def register_key(self, key, default_val, expire_time=5000):
        if not isinstance(key, str):
            raise TypeError('key:[%s] is not String' % key)
        if not isinstance(default_val, str):
            raise TypeError('key:[%s] must have default value and typeof default value muse be String!' % key)
        # 设置 key
        k = Key()
        k.value = default_val
        self.kv_pool[key] = k
        self.kv_pool[key].expire_time = expire_time

    # 根据key获取value
    def get_value(self, key):
        return self.kv_pool[key].value

    # 这个是事件循环，发现有数据过期，则调用函数去redis或mysql获取最新数据
    def _eventloop(self):
        while True:
            keys = self.get_expire_keys()
            # 如果长度为0，说明没有过期key，等待 0.1 秒后再查一遍
            if len(keys) == 0:
                time.sleep(0.1)
                continue
            # 如果能执行到这里，说明有过期的key，则去更新这些key
            self.update_keys(keys)

    # 开个线程，执行 _eventloop
    def create_thread(self):
        t1 = threading.Thread(target=self._eventloop, name='loop')
        t1.start()

    # 判断是否有数据过期，如果返回值是长度为0，则有，否则无
    def get_expire_keys(self):
        keys = []
        for key in self.kv_pool:
            # 如果过期了
            if self.kv_pool[key].is_expire():
                # 那么将key添加待更新list里
                keys.append(key)
        return keys

    # 更新keys
    def update_keys(self, keys):
        print('expire key is :%s' % keys)
        # 先从redis里取值更新，剩下返回的keys是redis无法更新到的，于是再从mysql里取值更新
        not_update_keys = self.query_redis(keys)
        # 再从 MySQL 里请求
        list = self.query_mysql(not_update_keys)
        for item in list:
            k = item['key']
            # 正确则更新数据
            if item['is_error'] is not True:
                self.kv_pool[k].value = item['value']
            else:
                # 错误的则设置重置该key的过期时间（值不变），在下次查询的时候再次查询，并写入日志（只写一次）
                self.kv_pool[k].value = self.kv_pool[k].value
                if self.kv_pool[k].ishave_write_error('sql') is not True:
                    self.kv_pool[k].set_write_error('sql', True)
                    log('key:[%s] read from mysql error!' % (k))
        self.update_redis(list)

    # 从redis请求，并返回取不到的
    def query_redis(self, keys):
        r = None
        # 连接redis服务器
        try:
            r = redis.Redis(**self._redis_args)
            expire_keys = []
            for key in keys:
                value = r.get(key)
                # 如果取不到值，则为None
                if value is not None:
                    self.kv_pool[key].value = value
                    print('key:[%s], get value:[%s]' % (key, value))
                else:
                    expire_keys.append(key)
        except BaseException as e:
            err = str(e)
            log(str(err))
        finally:
            if r is None:
                return
        return expire_keys

    # 更新 redis 里的值
    def update_redis(self, list):
        try:
            r = redis.Redis(**self._redis_args)
            for item in list:
                if item['is_error'] is False:
                    k = item['key']
                    # 设置这个key，并设置过期时间
                    e_time = int(self.kv_pool[k].expire_time / 1000)
                    r.set(k, item['value'], ex=e_time)
        except BaseException as e:
            err = str(e)
            log(str(err))

    # 从mysql里请求值
    def query_mysql(self, not_update_keys):
        list = []
        # print(self._mysql_args)
        with MySQLTool(**self._mysql_args) as m2:
            for k in not_update_keys:
                result2 = m2.run_sql([
                    ['SELECT * FROM key_value where k = %s', [k]]
                ])
                print('result2', result2)
                if result2 is False:
                    list.append({
                        'key': k,
                        'value': '',
                        'is_error': True
                    })
                else:
                    i = result2[0]
                    list.append({
                        'key': i[1],
                        'value': i[2],
                        'is_error': False
                    })
        return list


if __name__ == '__main__':
    # redis的配置
    r_config = {
        'host': '127.0.0.1',
        'port': 6379,
        'decode_responses': True,
        'password': ''
    }
    sql_config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '123456',
        'database': 'version_controller',
    }
    # 尝试导入自定义配置（这个是带密码的）
    try:
        from myconfig import redis_config, mysql_config

        r_config = redis_config
        sql_config = mysql_config
    except BaseException as e:
        pass

    # 创建实例
    c = KeyValueGetter(r_config, sql_config)
    # 注册key
    c.register_key('foo', 'default foo', expire_time=2000)
    # 查看当前值（即默认值），这里应该是 default foo
    print(c.get_value('foo'))


    # 测试用函数，循环打印要获取的值
    def test_fn():
        while True:
            print('-----------------------test_fn-----------------------')
            print(c.get_value('foo'))
            time.sleep(1)


    # 起个线程，一直打印，观看数据变化
    t2 = threading.Thread(target=test_fn, name='loop_test')
    t2.start()
