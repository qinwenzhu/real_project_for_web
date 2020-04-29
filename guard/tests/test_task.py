# -*- coding: utf-8 -*-
# @time: 2020/4/27 22:30 
# @Author: wenqinzhu
# @Email: zhuwenqin_vendor@sensetime.com
# @file: test_task.py
# @software: PyCharm

# 如果连续创建两次相同的任务，则前端提示语为：该设备已存在该类型任务，并点击取消按钮

import time
import pytest
from guard.datas.task_data import TaskData
from guard.pages.task_page import TaskPage
from guard.pages.components.table_list import TableListPage


def test_add_vehicle_illegally_parking_detection_task(task):
    # 测试添加-车辆违停任务
    TaskPage(task[0]).add_task_to_parked_vehicle(task_name=task[1]["task_name"], device_name=task[1]["device_name"],
                                                 time_minute=task[1]["time_minute"], timezone_name=None, attr_name=None)
    time.sleep(2)
    assert TableListPage(task[0]).judge_table_list_add_name(task[1]["task_name"])


def test_add_parking_detection_task_and_not_null(task_no_setup):
    # 测试添加车辆违停任务 - 非空校验
    TaskPage(task_no_setup).verify_parked_vehicle_not_null()
    time.sleep(2)

    result = [TaskPage(task_no_setup).dialog_error_info(flag="task"),
              TaskPage(task_no_setup).dialog_error_info(flag="device"),
              TaskPage(task_no_setup).dialog_error_info(flag="region")]

    assert "请输入正确格式的任务名称" in result[0]
    assert "请选择设备" in result[1]
    assert "请绘制违停区域" in result[2]


# @pytest.mark.skip("跳过")
def test_delete_vehicle_illegally_parking_detection_task(task):
    # 测试删除-车辆违停任务
    TableListPage(task[0]).operations_table_list(name=task[1]["task_name"], flag="delete")

    assert TableListPage(task[1]).judge_table_list_delete_name(task[1]["task_name"])
