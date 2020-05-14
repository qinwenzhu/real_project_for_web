# -*- coding: utf-8 -*-
# @time: 2020/4/27 22:30 
# @Author: wenqinzhu
# @Email: zhuwenqin_vendor@sensetime.com
# @file: test_task.py
# @software: PyCharm

import re
import time
import pytest
from guard.pages.classes.task import Task
from guard.pages.task_page import TaskPage
from guard.pages.record_page import RecordPage
from guard.pages.components.menubar import MenuBarPage
from guard.pages.components.table_list import TableListPage
pytestmark = pytest.mark.test


class TestStructCarTaskPositive:
    pytestmark = [pytest.mark.positive, pytest.mark.smoke]

    def test_add_vehicle_illegally_parking_detection_task(self, task):
        # 测试添加-车辆违停任务
        task_para = Task(task_name=task[1]["task_name"], device_name=task[1]["device_name"])
        TaskPage(task[0]).add_task_by_type(task_para, task_type="车辆-违停检测任务")
        assert TableListPage(task[0]).judge_table_list_add_name(task_para.task_name)

    @pytest.mark.usefixtures("close_dialog")
    def test_view_vehicle_illegally_parking_detection_task(self, task):
        # 测试查看-车辆违停任务
        TableListPage(task[0]).operations_table_list(name=task[1]["task_name"], flag="view")
        result = TaskPage(task[0]).verify_view_task_detail()
        assert task[1]["task_name"] == result

    @pytest.mark.usefixtures("close_dialog")
    def test_edit_vehicle_illegally_parking_detection_task(self, task):
        # 测试编辑-车辆违停任务，修改违停时限，验证任务是否能被正常修改
        time.sleep(1)
        TaskPage(task[0]).update_input_park_time(task_name=task[1]["task_name"])
        time.sleep(0.5)
        result = TaskPage(task[0]).verify_input_park_time(task_name=task[1]["task_name"])
        assert re.match(r"^.+[\u4E00-\u9FA5\s]+$", result)

    def test_update_task_state(self, task):
        # 测试更新当前新建任务的启用状态为：禁用
        time.sleep(2)
        TableListPage(task[0]).table_list_switch(name=task[1]["task_name"])
        assert TableListPage(task[0]).verify_state_success(name=task[1]["task_name"])

    @pytest.mark.usefixtures("back_default")
    def test_batch_disabled_task(self, task):
        # 测试任务的批量禁用操作
        TaskPage(task[0]).task_batch_operation(flag="disabled")
        assert TaskPage(task[0]).verify_operation_disabled_success()

    @pytest.mark.usefixtures("back_default")
    def test_batch_start_task(self, task):
        # 测试任务的批量启用操作
        TaskPage(task[0]).task_batch_operation(flag="start")
        time.sleep(0.5)
        assert TaskPage(task[0]).verify_operation_start_success()

    @pytest.mark.usefixtures("back_task_page")
    def test_view_task_push_record(self, task):
        # 查看任务在记录页面是否有推送记录
        time.sleep(2)
        RecordPage(task[0]).record_filter_by_device(device_name=task[1]["device_name"])
        time.sleep(1)
        if RecordPage(task[0]).verify_record_total == 0:
            # 强制等待一段时间后，再次点击筛选按钮，查看是否有记录推送
            time.sleep(10)
            RecordPage(task[0]).click_filter_or_reset_btn()
        assert RecordPage(task[0]).verify_record_total()

    def test_delete_vehicle_illegally_parking_detection_task(self, task):
        # 测试删除-车辆违停任务
        time.sleep(1)
        TableListPage(task[0]).operations_table_list(name=task[1]["task_name"], flag="delete")
        assert TableListPage(task[1]).judge_table_list_delete_name(task[1]["task_name"])

    @pytest.mark.usefixtures("back_default")
    @pytest.mark.skip("The number of tasks is zero！")
    def test_batch_delete_task(self, task):
        # 测试任务的批量删除操作
        time.sleep(3)
        TaskPage(task[0]).task_batch_operation(flag="delete", text="删除")
        time.sleep(0.5)
        assert TaskPage(task[0]).verify_operation_delete_success()


class TestStructPedestriansTaskPositive:
    pytestmark = [pytest.mark.positive, pytest.mark.smoke]

    def test_add_pedestrians_task(self, task):
        # 测试添加-行人区域入侵任务
        task_para = Task(task_name=task[1]["task_name"], device_name=task[1]["device_name"])
        TaskPage(task[0]).add_task_by_type(task_para, task_type="人体-区域闯入检测任务")
        assert TableListPage(task[0]).judge_table_list_add_name(task_para.task_name)

    @pytest.mark.usefixtures("close_dialog")
    def test_view_pedestrians_task(self, task):
        # 测试查看-行人区域入侵任务
        TableListPage(task[0]).operations_table_list(name=task[1]["task_name"], flag="view")
        result = TaskPage(task[0]).verify_view_task_detail()
        assert task[1]["task_name"] == result

    def test_delete_vehicle_illegally_parking_detection_task(self, task):
        # 测试删除-行人区域入侵任务
        TableListPage(task[0]).operations_table_list(name=task[1]["task_name"], flag="delete")
        assert TableListPage(task[1]).judge_table_list_delete_name(task[1]["task_name"])


@pytest.mark.negative
class TestStructCarTaskNegative:

    @pytest.mark.usefixtures("close_dialog")
    def test_add_parking_detection_task_and_not_null(self, task_no_setup):
        # 测试添加车辆违停任务 - 非空校验
        TaskPage(task_no_setup).verify_parked_vehicle_not_null()
        result = [TaskPage(task_no_setup).dialog_error_info(flag="task"),
                  TaskPage(task_no_setup).dialog_error_info(flag="device"),
                  TaskPage(task_no_setup).dialog_error_info(flag="region")]
        assert "请输入正确格式的任务名称" in result[0] and "请选择设备" in result[1] and "请绘制违停区域" in result[2]


@pytest.mark.negative
class TestStructPedestriansTaskNegative:
    # @pytest.mark.usefixtures("close_dialog")
    def test_add_pedestrians_task_and_not_null(self, task_no_setup):
        # 测试添加行人区域入侵任务 - 非空校验
        TaskPage(task_no_setup).verify_pedestrians_not_null()
        result = [TaskPage(task_no_setup).dialog_error_info(flag="task"),
                  TaskPage(task_no_setup).dialog_error_info(flag="device"),
                  TaskPage(task_no_setup).dialog_error_info(flag="region")]
        assert "请输入正确格式的任务名称" in result[0] and "请选择设备" in result[1] and "请绘制区域" in result[2]
