# -*- coding:utf-8 -*-
# @Time: 2020/4/21 19:12
# @Author: wenqin_zhu
# @File: test_device.py
# @Software: PyCharm

import time
import pytest
from guard.pages.device_page import DevicePage
from guard.pages.components.group_tree import GroupTreePage

from guard.pages.classes.web_global_info import GlobalDialogInfo


@pytest.mark.smoke
@pytest.mark.positive
class TestDevicePositive:

    def test_create_peer_device_group_from_default(self, device):
        # 测试从Default分组创建同级地图分组
        GroupTreePage(device[0]).create_peer_or_next_group(group_name=device[1]["device_group_name"], parent_name="Default")

        result = GlobalDialogInfo(device[0]).judge_alert_info()
        assert "创建同级分组成功" == result

    def test_add_device_to_camera(self, device):
        # 等待2秒并刷新页面
        device[0].refresh()
        time.sleep(2)
        DevicePage(device[0]).add_camera(device_type="网络摄像机", device_name=device[1]["device_name"], device_id=device[1]["device_id"],
                                         device_group_name=device[1]["device_group_name"], map_group_name=device[1]["map_group_name"],
                                         rtsp_address="rtsp://10.151.3.119:7554/IMG_0322.264", camera_type="RTSP")

        result = GlobalDialogInfo(device[0]).judge_alert_info()
        assert "添加设备成功" == result

