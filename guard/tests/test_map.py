# -*- coding:utf-8 -*-
# @Time: 2020/4/21 16:30
# @Author: wenqin_zhu
# @File: test_map.py
# @Software: PyCharm

import pytest
from guard.pages.map_page import MapPage
from guard.pages.components.group_tree import GroupTreePage
from guard.pages.classes.web_global_info import GlobalDialogInfo

from guard.pages.classes.custom_share_path import SharePath


class TestMapPositive:

    pytestmark = [pytest.mark.positive, pytest.mark.smoke]

    def test_create_peer_map_group_from_default(self, map_module):
        # 测试从Default分组创建同级地图分组
        GroupTreePage(map_module[0]).create_peer_or_next_group(group_name=map_module[1]["map_group_name"], parent_name="Default")

        result = GlobalDialogInfo(map_module[0]).judge_alert_info()
        assert "创建同级分组成功" == result

    def test_upload_map(self, map_module):
        # 测试在指定地图分组中上传地图

        # 上传地图
        MapPage(map_module[0]).upload_map(r"{}/map_data/company_4th_floor.jpg".format(SharePath.DATA_FOLDER), group_name=map_module[1]["map_group_name"])

        assert MapPage(map_module[0]).judge_upload_map_success()

    @pytest.mark.skip("跳过")
    @pytest.mark.usefixtures("del_sub_map_group_to_default")
    def test_create_next_map_group_suc_from_default(self, map_module, sole_group_name):
        # 测试从Default默认分组创建下一级地图分组

        if MapPage(map_module[0]).judge_upload_map_success() is False:
            # 如果当前分组下不存在地图，则进行创建
            GroupTreePage(map_module[0]).create_peer_or_next_group(group_name=sole_group_name, parent_name="Default",
                                                                   is_peer=False)
            result = GlobalDialogInfo(map_module[0]).judge_alert_info()
            assert "创建下一级分组成功" == result

    @pytest.mark.skip("跳过")
    @pytest.mark.usefixtures("close_next_map_group_tree_dialog")
    def test_create_next_map_group_fail_from_default(self, map_module, sole_group_name):
        # 测试从Default默认分组创建下一级地图分组

        if MapPage(map_module[0]).judge_upload_map_success() is True:
            # 需要先判断当前分组是否已经上传地图，如果已经上传地图，则断言该用例
            GroupTreePage(map_module[0]).create_peer_or_next_group(group_name=sole_group_name, parent_name="Default",
                                                               is_peer=False)

            result = GlobalDialogInfo(map_module[0]).judge_alert_info()
            assert "地图上存在设备" == result
