#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime


# key，默认属性参考 __init__
class Key(object):
    def __init__(self):
        # 值
        self._value = ''
        # 过期时间（ms），默认是5000，也可以手动设置
        self._expire_time = 5000
        # 上一次更新时间
        self.update_time = datetime.now().timestamp() * 1000
        # 当前key状态：pending：正在和redis、mysql交互，normal 正常
        self.status = 'normal'
        # 交互的的时间（默认为0，开始交互时，设置为datetime.now().timestamp() * 1000
        self.pending_time = 0
        # 是否曾写入错误日志（目的是避免重复写入日志）
        self.ishave_write_error_sql = False
        self.ishave_write_error_redis = False

    # 获取值
    @property
    def value(self):
        return self._value

    # 赋值
    @value.setter
    def value(self, value):
        self._value = value
        self.update_time = datetime.now().timestamp() * 1000
        self.status = 'normal'
        self.pending_time = 0

    @property
    def expire_time(self):
        return self._expire_time

    # 设置过期时间
    @expire_time.setter
    def expire_time(self, e_t):
        self._expire_time = e_t

    # 设置当前状态为配置中
    def set_status_pending(self):
        self.status = 'pending'
        self.pending_time = datetime.now().timestamp() * 1000

    # 是否更新中
    def is_pending(self):
        return self.status == 'pending'

    # 是否过期。时间过期，并且当前没有在更新数据中
    def is_expire(self):
        # 当前时间 - 上一次更新时间 > 过期时间
        if datetime.now().timestamp() * 1000 - self.update_time > self._expire_time:
            # 当前并且不在配置中
            if not self.is_pending():
                return True
        return False

    # 查询
    def ishave_write_error(self, type):
        if type == 'sql':
            return self.ishave_write_error_sql
        elif type == 'redis':
            return self.ishave_write_error_redis
        else:
            return False

    # 设置
    def set_write_error(self, type, result):
        if type == 'sql':
            self.ishave_write_error_sql = result
        elif type == 'redis':
            self.ishave_write_error_redis = result
        else:
            return False


if __name__ == '__main__':
    pass
