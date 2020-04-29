# -*- coding:utf-8 -*-
# @Time: 2020/3/18 18:10
# @Author: wenqin_zhu
# @File: handle_config.py
# @Software: PyCharm


import yaml
import os


class HandleConfig(object):
    """  读取配置文件 """

    def __init__(self, file_name):
        self.config = self.load_config(file_name)

    def load_config(self, file_name):
        if os.path.exists(file_name):
            with open(file_name, mode='r', encoding='utf-8') as file:
                configs = yaml.safe_load(file)
        else:
            with open(file_name, mode='w', encoding='utf-8') as file:
                configs = yaml.safe_load(file)

        # with open(path_to_config) as file:
        #     try:
        #         con_file = yaml.safe_load(file)
        #     except Exception as e:
        #         print("文件未找到！")
        #         raise
        return configs


if __name__ == '__main__':
    # 通过调取文件，测试封装方法
    import os
    # os.getcwd()   获取当前文件目录
    # os.path.split("目录地址")   对目录地址进行分离
    # os.path.split(os.getcwd())  对当前文件目录进行分离

    target, catalog = os.path.split(os.getcwd())
    # print(f"要获取的目标路径为：{target}")
    print(HandleConfig(f"{target}/guard/config/http_config.ym").config)
