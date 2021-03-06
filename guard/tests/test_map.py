# -*- coding:utf-8 -*-
# @Time: 2020/4/21 16:30
# @Author: wenqin_zhu
# @File: test_map.py
# @Software: PyCharm

import re
import pytest
from guard.pages.map_page import MapPage
from guard.pages.classes.path import SharePath
from guard.pages.components.group_tree import GroupTreePage
from guard.pages.components.alert_info import AlertInfoPage

pytestmark = pytest.mark.test


class TestMapPositive:

    pytestmark = [pytest.mark.positive, pytest.mark.smoke]

    def test_create_peer_map_group_from_default(self, map_module):
        # 测试从Default分组创建同级地图分组
        GroupTreePage(map_module[0]).create_peer_or_next_group(group_name=map_module[1]["map_group_name"])
        result = AlertInfoPage(map_module[0]).get_alert_info()
        assert "创建同级分组成功" == result

    def test_upload_map(self, map_module):
        # 测试在指定地图分组中上传地图
        # 上传地图
        MapPage(map_module[0]).upload_map(r"{}/map_data/company_4th_floor.jpg".format(SharePath.DATA_FOLDER), group_name=map_module[1]["map_group_name"])
        assert MapPage(map_module[0]).is_upload_map_success()

    def test_create_peer_map_from_user_defined(self, map_module, sole_group_name):
        # 测试从用户自定义分组创建同级分组
        GroupTreePage(map_module[0]).create_peer_or_next_group(group_name=sole_group_name, parent_name=map_module[1]["map_group_name"])
        result = AlertInfoPage(map_module[0]).get_alert_info()
        assert "创建同级分组成功" == result

    def test_create_next_map_from_user_defined(self, map_module, sole_group_name):
        # 测试从用户自定义分组创建下一级分组
        GroupTreePage(map_module[0]).create_peer_or_next_group(group_name=sole_group_name, parent_name=map_module[1]["map_group_name"], is_peer=False)
        result = AlertInfoPage(map_module[0]).get_alert_info()
        assert "创建下一级分组成功" == result

    @pytest.mark.usefixtures("close_dialog")
    def test_create_next_map_group_from_default(self, map_module, sole_group_name):
        # 测试从Default默认分组创建下一级地图分组
        GroupTreePage(map_module[0]).create_peer_or_next_group(group_name=sole_group_name, parent_name="Default",
                                                               is_peer=False)
        result = AlertInfoPage(map_module[0]).get_alert_info()
        # print(result)
        # print(MapPage(map_module[0]).map_group_is_exist_device())
        """ 条件判断：如果Default分组下存在设备，则断言A，否则断言B，默认返回True，存在设备 """
        if MapPage(map_module[0]).map_group_is_exist_device() is True:
            assert "地图上存在设备" == result
        else:
            assert "创建下一级分组成功" == result

    def test_search_dep_by_name(self, map_module):
        # 测试group_tree的搜索功能
        GroupTreePage(map_module[0]).search_dep_by_name(map_module[1]["map_group_name"])
        result = GroupTreePage(map_module[0]).judge_search_success(map_module[1]["map_group_name"])
        assert re.match("^FGN-[0-9a-zA-Z]+.{3}", result)

    def test_delete_peer_map_group_from_default(self, map_module):
        # 测试从Default分组删除同级地图分组
        GroupTreePage(map_module[0]).delete_peer_or_next_group_by_name(module_val="map", parent_name=map_module[1]["map_group_name"])
        result = AlertInfoPage(map_module[0]).get_alert_info()
        assert "删除分组成功！" == result
