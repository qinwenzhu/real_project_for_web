# -*- coding:utf-8 -*-
# @Time: 2020/4/1 18:57
# @Author: wenqin_zhu
# @File: test_user.py
# @Software: PyCharm

import re
import pytest
from guard.pages.classes.web_global_info import GlobalDialogInfo
from guard.pages.components.group_tree import GroupTreePage


class TestUserPositive:

    pytestmark = [pytest.mark.positive, pytest.mark.smoke]

    @pytest.mark.usefixtures("close_alert")
    def test_create_peer_dep_from_default(self, user):
        # 测试从Default根分组创建同级分组
        GroupTreePage(user[0]).create_peer_or_next_group(group_name=user[1], parent_name="Default")

        result = GlobalDialogInfo(user[0]).judge_alert_info()
        assert "创建同级分组成功" == result

    @pytest.mark.skip("跳过")
    @pytest.mark.usefixtures("close_alert", "del_sub_dep_name_to_user")
    def test_create_next_dep_from_user_defined(self, user, sole_group_name):
        # 测试从用户自定义分组创建下一级分组
        GroupTreePage(user[0]).create_peer_or_next_group(group_name=sole_group_name, parent_name=user[1], is_peer=False)

        result = GlobalDialogInfo(user[0]).judge_alert_info()
        assert "创建下一级分组成功" == result

    @pytest.mark.skip("跳过")
    @pytest.mark.usefixtures("close_alert", "del_dep_name_to_user")
    def test_create_peer_dep_from_user_defined(self, user, sole_group_name):
        # 测试从用户自定义分组创建同级分组
        GroupTreePage(user[0]).create_peer_or_next_group(group_name=sole_group_name, parent_name=user[1])

        result = GlobalDialogInfo(user[0]).judge_alert_info()
        assert "创建同级分组成功" == result

    @pytest.mark.skip("跳过")
    @pytest.mark.usefixtures("close_alert", "del_sub_dep_name_to_default")
    def test_create_next_dep_from_default(self, user, sole_group_name):
        # 测试从Default根分组创建下一级分组
        GroupTreePage(user[0]).create_peer_or_next_group(group_name=sole_group_name, parent_name="Default", is_peer=False)

        result = GlobalDialogInfo(user[0]).judge_alert_info()
        assert "创建下一级分组成功" == result

    def test_search_dep_by_name(self, user):
        # 测试group_tree的搜索功能
        GroupTreePage(user[0]).search_dep_by_name(user[1])

        # 断言搜索到的内容<前端缩略显示的>在user字符串内
        result = GroupTreePage(user[0]).judge_search_success(user[1])
        # print(result)
        assert re.match("^UDN-[0-9a-zA-Z]+.{3}", result)
        """
        # 此时使用正则表达式进行匹配结果
        # ^UDN-[0-9a-zA-Z]{6}.{3}
        # ^UDN-：以UDN-开头； [0-9a-zA-Z]+：0-9/a-z/A-Z匹配数字6次，+代表1次或多次； .{3}：匹配除换行符以外的字符，此处用于匹配点号，匹配3次
        """

    @pytest.mark.usefixtures("close_alert")
    def test_delete_peer_dep_from_default(self, user):
        GroupTreePage(user[0]).delete_peer_or_next_group_by_name(parent_name=user[1], module_val="user")

        result = GlobalDialogInfo(user[0]).judge_alert_info()
        assert "删除分组成功" == result
