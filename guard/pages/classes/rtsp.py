# -*- coding:utf-8 -*-
# @Time: 2020/5/7 10:57
# @Author: wenqin_zhu
# @File: rtsp.py
# @Software: PyCharm

from guard.pages.classes.device import Device


class Rtsp(Device):

    def __init__(self, device_name, device_id, group_name, floor_name, rtsp_address):
        """
        继承Device，并在此基础上进行扩展
        :param device_name:
        :param device_id:
        :param group_name:
        :param floor_name:
        :param rtsp_address: rtsp地址
        """

        """ 重写device在子类的几种调用方式 """
        # 直接通过父类名调用
        # Device.__init__(self, device_name, device_id, group_name, floor_name)

        # 直接通过super,然后在标注子类名调用父类的init方法
        # super(Rtsp, self).__init__(device_name, device_id, group_name, floor_name)

        # 在继承父类的基础上对方法进行扩展
        super().__init__(device_name, device_id, group_name, floor_name)
        self.__rtsp_address = rtsp_address

    @property
    def rtsp_address(self):
        return self.__rtsp_address

    @rtsp_address.setter
    def rtsp_address(self, value):
        self.__rtsp_address = value
