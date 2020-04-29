#!/usr/bin/python3
# -*- coding: utf-8 -*-

import redis
import logging


class GetRedisData(object):

    # def __init__(self, ip, port=6379):
    def __init__(self, ip, port=30379):
        """
        连接Redis
        :param ip:
        :param port:
        """
        try:
            # pool = redis.ConnectionPool(host=ip, port=port, db=0)
            pool = redis.ConnectionPool(host=ip, port=port, db=0, password='9@mXWb%m8w5n')
            self.conn = redis.StrictRedis(connection_pool=pool)
        except Exception as err:
            logging.error("connect Redis failed: %s" % err)

    def get_result_from_redis(self, key):
        keys = self.conn.keys()
        # print(f"获取到的当前连接池内所有的keys值为：{keys}")
        if bytes(key, encoding="utf8") in keys:
            # 获取到正则匹配到的key
            result = self.conn.get(key)
            logging.info("{}的redis值为：{}".format(key, result))

            # print(f"获取到的当前验证码为：{result.decode()}")
            return result.decode()
        else:
            logging.error('key "{}" has no result found in Redis!'.format(key))
            return False

    # def set_value_to_redis(self, key, value):
    #     try:
    #         key_val = self.conn.set(key, str(value))
    #         # assert (self.conn.get(key).decode("utf-8") == value), "set {} error".format(key)
    #     except Exception as err:
    #         logging.error("Redis设置{}值出错{}".format(key, err))
    #     else:
    #         return key_val
