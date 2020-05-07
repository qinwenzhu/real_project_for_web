# -*- coding:utf-8 -*-
# @Time: 2020/5/7 15:28
# @Author: wenqin_zhu
# @File: task.py
# @Software: PyCharm


class Task(object):

    def __init__(self, task_name, device_name, special_attributes: list = []):
        self.__task_name = task_name
        self.__device_name = device_name
        self.__special_attributes = special_attributes

    @property
    def task_name(self):
        return self.__task_name

    @task_name.setter
    def task_name(self, value):
        self.__task_name = value

    @property
    def device_name(self):
        return self.__device_name

    @device_name.setter
    def device_name(self, value):
        self.__device_name = value

    @property
    def special_attributes(self):
        return self.__special_attributes

    @special_attributes.setter
    def special_attributes(self, value):
        self.__special_attributes = value
