# -*- coding:utf-8 -*-
# @Time: 2020/4/20 17:59
# @Author: wenqin_zhu
# @File: task_page.py
# @Software: PyCharm

import time
from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage
from selenium.webdriver.common.action_chains import ActionChains
from guard.pages.classes.web_com_content_click import WebContentClick as click_btn


class TaskPage(BasePage):

    def click_left_menu(self, menu_name):
        """ 点击左侧任务菜单 """
        TASK_MENU = (By.XPATH, f'//div[@class="task-menu-container"]//li[contains(text(), "{menu_name}")]')
        BasePage(self.driver).click_ele(TASK_MENU)

    def add_task_to_parked_vehicle(self, task_name, device_name, time_minute, timezone_name=None, attr_name=None, menu_name="车辆-违停检测任务", is_confirm=True):
        """
        添加车辆违停任务
        :param task_name: 任务名称
        :param device_name: 设备名称
        :param time_minute: 违停时长
        :param timezone_name: 时间条件名称
        :param attr_name: 特殊属性
        :param menu_name: 任务类型
        :param is_confirm: 是否添加任务，默认添加
        """
        # 点击左侧菜单
        self.click_left_menu(menu_name)
        # 点击添加任务
        click_btn(self.driver).click_btn(btn_name="添加任务")
        # 基础配置
        self.select_task_type(menu_name)
        self.input_task_name(task_name)
        self.select_device(device_name)
        self.select_timezone(timezone_name)
        self.select_special_attr(attr_name)
        self.input_park_time(time_minute)
        self.com_car_size("最小车辆识别尺寸", width=30, height=30)
        self.com_car_size("最大车辆识别尺寸", width=500, height=500)
        self.draw_park_region()

        if is_confirm:
            # 点击确定
            self.com_confirm_or_cancel(is_confirm=is_confirm)
        else:
            # 点击取消
            self.com_confirm_or_cancel(is_confirm=is_confirm)

    def com_confirm_or_cancel(self, til_name="添加任务", is_confirm=True):
        if is_confirm:
            # 点击确定
            CONFIRM_BTN = (By.XPATH, f'//div[@aria-label="{til_name}"]//div[@class="el-dialog__footer"]//span[contains(text(), "确定")]')
            BasePage(self.driver).click_ele(CONFIRM_BTN)
        else:
            # 点击取消
            CANCEL_BTN = (By.XPATH, f'//div[@aria-label="{til_name}"]//div[@class="el-dialog__footer"]//span[contains(text(), "取消")]')
            BasePage(self.driver).click_ele(CANCEL_BTN)

    # 定位-任务类型
    def select_task_type(self, task_type):
        # 此处，采用的是先点击左侧对应的菜单，所以次数不需要下拉选择
        TASK_DEVICE = (By.XPATH, '//label[contains(text(), "任务类型")]/following-sibling::div//input')
        BasePage(self.driver).click_ele(TASK_DEVICE)
        # 定位任务类型
        SELECT_TASK_DEV = (By.XPATH, f'//span[text()="{task_type}"]')
        # 移动到任务累心上并进行选择
        BasePage(self.driver).mouse_move_ele_and_click(TASK_DEVICE, SELECT_TASK_DEV)

    # 定位-任务名称
    def input_task_name(self, task_name):
        NAME = (By.XPATH, '//label[contains(text(), "任务名称")]/following-sibling::div//input')
        BasePage(self.driver).update_input_text(NAME, task_name)

    # 定位-设备，为指定设备绑定任务
    def select_device(self, device_name):

        DEVICE = (By.XPATH, '//label[contains(text(), "设备")]/following-sibling::div//div[contains(@class, "el-popover__reference")]//input')
        BasePage(self.driver).click_ele(DEVICE)

        # 通过设备名搜索设备并选择
        self.comm_search_result_by_name(device_name)

    # 定位-时间条件
    def select_timezone(self, timezone_name):
        """
        选择时间条件名
        :param timezone_name: 通过设置好的timezone名，选择对应的时间条件
        """
        # 定位时间条件选择框
        TIMEZONE = (By.XPATH, '//label[contains(text(), "时间条件")]/following-sibling::div//input')
        BasePage(self.driver).click_ele(TIMEZONE)
        if timezone_name is not None:
            # 如果时间条件不为空，则进行时间条件的选择

            # 通过timezone的名称，定位时间条件
            SELECT_TIMEZONE = (By.XPATH, f'//span[text()="{timezone_name}"]')
            BasePage(self.driver).mouse_move_ele_and_click(TIMEZONE, SELECT_TIMEZONE)
        else:
            # 否则直接点击选择框，不进行选择
            BasePage(self.driver).click_ele(TIMEZONE)

    # 定位-特殊属性
    def select_special_attr(self, attr_name: list):
        """  特殊属性支持多选：入口，出口，第三方对接 """

        # 定位特殊属性选择框
        SPECIAL_ATTR = (By.XPATH, '//label[contains(text(), "特殊属性")]/following-sibling::div//input')
        BasePage(self.driver).click_ele(SPECIAL_ATTR)

        if attr_name is not None:
            # 通过指定特殊属性的名称，进行选择
            SELECT_ATTR = (By.XPATH, f'//span[text()="{attr_name}"]')
            # 移动到特殊属性下拉列表上并进行选择
            BasePage(self.driver).mouse_move_ele_and_click(SPECIAL_ATTR, SELECT_ATTR)
        else:
            BasePage(self.driver).click_ele(SPECIAL_ATTR)

    # 定位-违停时限
    def input_park_time(self, time_minute=1):
        PARK_TIME = (By.XPATH, '//label[contains(text(), "违停时限")]/following-sibling::div//input')
        # 先清空输入框内的数值
        BasePage(self.driver).clear_input_default_val(PARK_TIME)
        # 再输入目标分钟数
        BasePage(self.driver).update_input_text(PARK_TIME, time_minute)

    # 定位-最小/最大车辆识别尺寸
    def com_car_size(self, text_name, width=30, height=30):
        # 定位宽
        SIZE_WIDTH = (By.XPATH, f'//label[contains(text(), "{text_name}")]/following-sibling::div//label[text()="宽"]/following-sibling::div//input')
        # 定位高
        SIZE_HEIGHT = (By.XPATH, f'//label[contains(text(), "{text_name}")]/following-sibling::div//label[text()="高"]/following-sibling::div//input')
        # 先清空input框中的默认数值
        BasePage(self.driver).clear_input_default_val(SIZE_WIDTH)
        BasePage(self.driver).clear_input_default_val(SIZE_HEIGHT)
        # 进行数值输入
        BasePage(self.driver).update_input_text(SIZE_WIDTH, width)
        BasePage(self.driver).update_input_text(SIZE_HEIGHT, height)

    # 定位-区域绘制
    def draw_park_region(self):
        # 定位点击绘制区域的按钮
        REGION_BTN = (By.XPATH, '//i/parent::div[contains(text(), "点击绘制区域 ")]')
        BasePage(self.driver).click_ele(REGION_BTN)
        # 滚动到视频违停区域
        VIEW_REGION = (By.XPATH, '//div[@class="addTaskPC-video"]')
        BasePage(self.driver).scroll_visibility_region(loc=VIEW_REGION)
        time.sleep(2)
        # 绘制违停区域
        PARK_REGION = (By.CSS_SELECTOR, '.draw-line')
        ele = BasePage(self.driver).get_ele_locator(PARK_REGION)

        # 参数形式
        draw_param = [(-100, -100), (100, -100), (100, 100), (-100, 100), (-100, -100)]
        for point in draw_param:
            self.draw_line(point[0], point[1], ele)

    """ ---------------------------- 页面共用封装方法 ---------------------------- """
    def comm_search_result_by_name(self, name):
        """  任务下拉列表搜索 """
        # 1、通过设备名device_name,查找设备
        SELECT_GROUP = (By.XPATH,
                        '//div[@role="tooltip" and contains(@style, "position")]//div[contains(@class, "el-input")]//input')
        BasePage(self.driver).update_input_text(SELECT_GROUP, name)

        # 2、通过设备名device_name, 定位到查询结果
        RESULT = (By.XPATH, f'//span[@class="el-radio__label"]//span[@title="{name}"]')
        # 点击到查询的设备分组名
        BasePage(self.driver).click_ele(RESULT, timeout=20)

    def draw_line(self, x_offset, y_offset, ele):
        actions = ActionChains(self.driver)
        actions.move_to_element(ele)
        actions.perform()
        actions.pause(1)
        actions.move_by_offset(x_offset, y_offset)
        actions.perform()
        actions.pause(1)
        actions.click()
        actions.perform()

    def dialog_error_info(self, flag="task"):
        # 通过不同的flag定位不同的错误信息元素定位表达式，并返回错误信息
        ERROR_INFO = (By.XPATH, '//div[@class="el-form-item__error"]')
        if flag == "task":
            # 如果是校验设备名的错误信息，下标为0
            ele = BasePage(self.driver).get_ele_locator_by_index(ERROR_INFO, 0)
        elif flag == "device":
            ele = BasePage(self.driver).get_ele_locator_by_index(ERROR_INFO, 1)
        elif flag == "region":
            ele = BasePage(self.driver).get_ele_locator_by_index(ERROR_INFO, 2)
        return ele.text

    def click_close_dialog_btn(self):
        """  点击关闭dialog窗口 """
        # 定位关闭弹窗
        CLOSE_BUTTON = (By.XPATH, '//div[@class="el-dialog__wrapper"]//span[contains(text(), "添加任务")]/following-sibling::button')
        BasePage(self.driver).click_ele(CLOSE_BUTTON)

    """------------------ 非空校验 ---------------------------"""
    def verify_parked_vehicle_not_null(self, is_confirm=True):
        """ 点击添加任务，点击确认，进行车辆违停的非空校验"""
        # 点击左侧菜单
        self.click_left_menu("车辆-违停检测任务")
        click_btn(self.driver).click_btn(btn_name="添加任务")
        self.com_confirm_or_cancel(is_confirm=is_confirm)

    # def verify_parked_vehicle_not_null_device_name(self, device_name, menu_name="车辆-违停检测任务", is_confirm=True):
    #     点击左侧菜单
    #     self.click_left_menu(menu_name)
    #     # 点击添加任务
    #     click_btn(self.driver).click_btn(btn_name="添加任务")
    #     # 基础配置
    #     # self.select_task_type(menu_name)
    #     self.input_task_name(task_name)
    #
    #     self.select_device()
    #     self.com_confirm_or_cancel(is_confirm=is_confirm)


if __name__ == '__main__':
    from selenium import webdriver
    from guard.pages.login_page import LoginPage
    from guard.pages.components.menubar import MenubarPage

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://10.151.3.96/login")
    LoginPage(driver).login("zhuwenqin", "888888", login_way="debug")
    MenubarPage(driver).click_nav_item("配置", "任务管理")
    TaskPage(driver).add_task_to_parked_vehicle(task_name="test", device_name="1111", time_minute=1)

    # from guard.pages.components.table_list import TableListPage
    # TaskPage(driver).click_left_menu("车辆-违停检测任务")
    # TableListPage(driver).operations_table_list(name="id-2b244f07-cb55-47e7-87ef-3dca9ca47593", flag="delete")
