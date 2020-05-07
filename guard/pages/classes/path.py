# -*- coding:utf-8 -*-
# @Time: 2020/3/19 14:33
# @Author: wenqin_zhu
# @File: path.py
# @Software: PyCharm

"""
项目共享路径
"""
import os


class SharePath:

    # 获取当前文件的绝对路径
    current_path = os.path.abspath(__file__)
    """ 通过 os.path.split() 对路径进行逐级分割直至获取到项目的根目录 """
    PRO_PATH = os.path.split(os.path.split(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])[0])[0]
    # print(PRO_PATH)

    # 定位到 configs 目录
    CONFIG_FOLDER = f"{PRO_PATH}/guard/configs"

    # 定位到 datas 目录
    DATA_FOLDER = f"{PRO_PATH}/guard/datas"

    # 定位到 logs 目录
    LOG_FOLDER = f"{PRO_PATH}/outputs/logs"

    # 定位到屏幕截图 <screenshots> 目录
    SCREENSHOT_FOLDER = f"{PRO_PATH}/outputs/screenshots"
