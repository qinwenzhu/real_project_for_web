# -*- coding:utf-8 -*-
# @Time: 2020/4/16 16:10
# @Author: wenqin_zhu
# @File: run_env.py
# @Software: PyCharm

from guard.pages.classes.path import SharePath
from utils.handle_config import HandleConfig


def env():
    # 读取当前的测试环境
    IP_CONFIG = HandleConfig(r'{}\run_env_config.yml'.format(SharePath.CONFIG_FOLDER)).config
    # 返回当前执行测试的环境和测试登录用户
    """
    测试环境/登录用户动态更换
    {'host': '10.151.3.96', 'username': 'zhuwenqin', 'password': '888888'}
    """
    return IP_CONFIG.get("operation")
