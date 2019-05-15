#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from package.redis_lingling import KeyValueGetter

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
    from package.redis_lingling.myconfig import redis_config, mysql_config

    r_config = redis_config
    sql_config = mysql_config
except BaseException as e:
    pass

# 创建实例
c = KeyValueGetter(r_config, sql_config)
