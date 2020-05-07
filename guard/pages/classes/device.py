# -*- coding:utf-8 -*-
# @Time: 2020/5/7 10:48
# @Author: wenqin_zhu
# @File: device.py
# @Software: PyCharm


class Device(object):

    def __init__(self, device_name, device_id, group_name, floor_name):
        """
        初始化设备基础变量
        :param device_name: 设备名称
        :param device_id: 设备ID
        :param group_name: 设备分组名称
        :param floor_name: 楼层分组名称
        """
        self.__device_name = device_name
        self.__device_id = device_id
        self.__group_name = group_name
        self.__floor_name = floor_name

    @property
    def device_name(self):
        return self.__device_name

    @device_name.setter
    def device_name(self, value):
        self.__device_name = value

    @property
    def device_id(self):
        return self.__device_id

    @device_id.setter
    def device_id(self, value):
        self.__device_id = value

    @property
    def group_name(self):
        return self.__group_name

    @group_name.setter
    def group_name(self, value):
        self.__group_name = value

    @property
    def floor_name(self):
        return self.__floor_name

    @floor_name.setter
    def floor_name(self, value):
        self.__floor_name = value
