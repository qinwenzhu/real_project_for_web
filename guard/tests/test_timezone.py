# -*- coding:utf-8 -*-
# @Time: 2020/4/13 14:19
# @Author: wenqin_zhu
# @File: test_timezone.py
# @Software: PyCharm

import re
import time
import pytest
from guard.pages.timezone_page import TimezonePage
from guard.pages.components.alert_info import AlertInfoPage


# 正向测试用例
class TestTimezonePositive:
    """
    pytest给测试类打标记的功能，单个标记以及多个标记
        # 给测试类打标记
        # pytestmark = pytest.mark.positive
    """
    # 如果一个测试类有多个标记的话，采用多标记功能
    pytestmark = [pytest.mark.positive, pytest.mark.smoke]

    def test_add_timezone(self, connect_mysql_and_close, timezone):
        # 测试添加时间条件
        TimezonePage(timezone[0]).add_timezone(timezone[1]["timezone"])
        # 断言
        sql = "SELECT * FROM senseguard.info_time_zone WHERE time_zone_name=%s;"
        # 优化：鼠标总是移动到删除按钮失败，强制等待2秒
        time.sleep(2)
        result = connect_mysql_and_close.select_database(sql, args=(timezone[1]["timezone"], ))
        # print(f"数据库查询结果为：{result}")
        assert timezone[1]["timezone"] == result["time_zone_name"]

    def test_add_timezone_section(self, timezone):
        # 通过选择 指定的时间条件名称 创建时间段
        TimezonePage(timezone[0]).add_timezone_section_by_timezone_name(timezone[1]["timezone"])
        # 断言
        result = TimezonePage(timezone[0]).assert_timezone_section()
        assert re.match(r'\d+:\d+-\d+:\d', result)

    def test_create_holidays(self, connect_mysql_and_close, timezone):
        # 测试添加假期
        TimezonePage(timezone[0]).create_holidays("添加假期", timezone[1]["holiday_name"], num=1)
        # 断言
        sql = "SELECT * FROM senseguard.info_holiday WHERE holiday_name=%s;"
        time.sleep(2)
        result = connect_mysql_and_close.select_database(sql, args=(timezone[1]["holiday_name"], ))
        # print(f"数据库查询结果为：{result}")
        assert timezone[1]["holiday_name"] == result["holiday_name"]

    def test_create_workday(self, connect_mysql_and_close, timezone):
        # 测试添加特殊工作日
        TimezonePage(timezone[0]).create_workday("添加特殊工作日", timezone[1]["workday_name"], num=1)
        # 断言1：通过数据库查询
        sql = "SELECT * FROM senseguard.info_holiday WHERE holiday_name=%s;"
        time.sleep(2)
        result = connect_mysql_and_close.select_database(sql, args=(timezone[1]["workday_name"], ))
        # print(f"数据库查询结果为：{result}")
        assert timezone[1]["workday_name"] == result["holiday_name"]
        # 断言2：通过获取添加动作之后的页面元素的text来断言 - 两个断言条件都可以断言成功，
        text_result = TimezonePage(timezone[0]).assert_result_by_name(timezone[1]["workday_name"])
        assert timezone[1]["workday_name"] in text_result


class TestTimezoneNegative:

    # 给测试类打共用标记
    pytestmark = pytest.mark.negative

    @pytest.mark.usefixtures("close_alert_info")
    def test_add_timezone_and_beyond(self, timezone, overlong_name):
        # 测试添加事件条件的超出指定字符长度
        TimezonePage(timezone[0]).add_timezone(overlong_name)
        # 断言
        result = AlertInfoPage(timezone[0]).get_alert_info()
        assert "请输入最多40个字符的时间条件名称" == result

    def test_add_same_name_to_timezone(self, timezone):
        # 测试添加同名的时间条件
        TimezonePage(timezone[0]).add_timezone(timezone[1]["timezone"])
        # 断言
        result = AlertInfoPage(timezone[0]).get_alert_info()
        assert "资源被占用或不存在" == result

    def test_add_holidays_negative_conflict(self, timezone, overlong_name):
        # 测试添加假期与页面现有的假期时间冲突
        TimezonePage(timezone[0]).create_holidays("添加假期", overlong_name)
        # 断言
        result = AlertInfoPage(timezone[0]).get_alert_info()
        assert "创建的假期与已有的假期有冲突，请检查后重新设置" == result

    def test_add_workday_negative_conflict(self, timezone, overlong_name):
        # 测试添加特殊工作日与页面现有的工作日时间冲突
        TimezonePage(timezone[0]).create_workday("添加特殊工作日", overlong_name)
        # 断言
        result = AlertInfoPage(timezone[0]).get_alert_info()
        assert "创建的特殊工作日与已有的特殊工作日有冲突，请检查后重新设置" == result


@pytest.mark.smoke
@pytest.mark.positive
def test_delete_timezone(timezone):
    # 删除时间条件
    TimezonePage(timezone[0]).delete_or_rename_timezone_name(timezone[1]["timezone"])
    assert TimezonePage(timezone[0]).judge_delete_success(timezone[1]["timezone"])


@pytest.mark.smoke
@pytest.mark.positive
def test_delete_holiday(timezone):
    # 删除假期
    TimezonePage(timezone[0]).delete_or_rename_holidays_or_workday(timezone[1]["holiday_name"])
    assert TimezonePage(timezone[0]).judge_delete_success(timezone[1]["holiday_name"])


@pytest.mark.smoke
@pytest.mark.positive
def test_delete_workday(timezone):
    # 删除特殊工作日
    TimezonePage(timezone[0]).delete_or_rename_holidays_or_workday(timezone[1]["workday_name"])
    assert TimezonePage(timezone[0]).judge_delete_success(timezone[1]["workday_name"])


if __name__ == '__main__':
    pytest.main()
