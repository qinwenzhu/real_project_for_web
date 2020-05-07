# -*- coding: utf-8 -*-
# @time: 2020/4/27 22:30 
# @Author: wenqinzhu
# @Email: zhuwenqin_vendor@sensetime.com
# @file: test_task.py
# @software: PyCharm

import time
import pytest
from guard.pages.classes.task import Task
from guard.pages.task_page import TaskPage
from guard.pages.components.table_list import TableListPage


class TestStructTaskPositive:

    pytestmark = [pytest.mark.positive, pytest.mark.smoke]

    def test_add_vehicle_illegally_parking_detection_task(self, task):
        task_para = Task(task_name=task[1]["task_name"], device_name=task[1]["device_name"])
        TaskPage(task[0]).add_task_by_type(task_para, task_type="车辆-违停检测任务")

        time.sleep(2)
        assert TableListPage(task[0]).judge_table_list_add_name(task_para.task_name)

    def test_delete_vehicle_illegally_parking_detection_task(self, task):
        # 测试删除-车辆违停任务
        TableListPage(task[0]).operations_table_list(name=task[1]["task_name"], flag="delete")

        assert TableListPage(task[1]).judge_table_list_delete_name(task[1]["task_name"])


class TestStructTaskNegative:

    # @pytest.mark.usefixtures("close_add_task_dialog_btn")
    def test_add_parking_detection_task_and_not_null(self, task_no_setup):
        # 测试添加车辆违停任务 - 非空校验
        TaskPage(task_no_setup).verify_parked_vehicle_not_null()
        time.sleep(2)
        result = [TaskPage(task_no_setup).dialog_error_info(flag="task"),
                  TaskPage(task_no_setup).dialog_error_info(flag="device"),
                  TaskPage(task_no_setup).dialog_error_info(flag="region")]
        assert "请输入正确格式的任务名称" in result[0] and "请选择设备" in result[1] and "请绘制违停区域" in result[2]
