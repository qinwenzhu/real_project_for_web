# -*- coding:utf-8 -*-
# @Time: 2020/4/21 19:12
# @Author: wenqin_zhu
# @File: test_device.py
# @Software: PyCharm

import time
import pytest
from guard.pages.classes.rtsp import Rtsp
from guard.pages.device_page import DevicePage
from guard.pages.components.group_tree import GroupTreePage
from guard.pages.components.alert_info import AlertInfoPage

pytestmark = pytest.mark.test


class TestDevicePositive:

    pytestmark = [pytest.mark.smoke, pytest.mark.positive]

    def test_create_peer_device_group_from_default(self, device):
        # 创建完地图的页面直接调整，页面尚未加载完毕
        time.sleep(1)
        # 测试从Default分组创建同级设备分组
        GroupTreePage(device[0]).create_peer_or_next_group(group_name=device[1]["device_group_name"])

        result = AlertInfoPage(device[0]).get_alert_info()
        assert "创建同级分组成功" == result

    def test_add_device_and_type_is_rtsp(self, device, uuid4_para):
        device_param = Rtsp(device_name=uuid4_para, device_id=uuid4_para, group_name=device[1]["device_group_name"],
                            floor_name=device[1]["floor_group_name"], rtsp_address="rtsp://10.151.3.119:7554/IMG_0322.264")
        DevicePage(device[0]).add_device_by_type(device=device_param, device_type="网络摄像机")

    def test_delete_peer_device_group_from_default(self, device):
        # 测试从Default分组删除同级设备分组
        time.sleep(1)
        GroupTreePage(device[0]).delete_peer_or_next_group_by_name(module_val="device", parent_name=device[1]["device_group_name"])

        result = AlertInfoPage(device[0]).get_alert_info()
        assert "删除分组成功" == result
