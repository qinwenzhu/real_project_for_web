# -*- coding:utf-8 -*-
# @Time: 2020/4/20 17:59
# @Author: wenqin_zhu
# @File: task_page.py
# @Software: PyCharm

import time
from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage
from guard.pages.components.dialog import DialogPage
from selenium.webdriver.support.wait import WebDriverWait
from guard.pages.components.table_list import TableListPage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class TaskPage(BasePage):

    def add_task_by_type(self, task, task_type, is_confirm=True):

        # 点击任务左侧菜单
        self.click_left_menu(menu_name=task_type)
        # 点击添加任务按钮
        self.click_add_task_btn()
        # 选择任务类型
        self.select_task_type(task_type=task_type)
        """ 开始添加任务界面的基础共用操作：任务名称、设备名称、设备分组，选择特殊属性 """
        self.task_basic_set(task)

        if task_type == "车辆-违停检测任务":
            # 设置违停时限
            self.input_park_time()
            # 绘制违停区域
            self.draw_park_region()
        elif task_type == "人体-区域闯入检测任务":
            # 绘制违停区域
            self.draw_park_region()
        elif task_type == "人体-越线检测任务":
            pass

        # 点击确认或取消按钮
        if is_confirm:
            DialogPage(self.driver).is_confirm_or_cancel("添加任务")
        else:
            DialogPage(self.driver).is_confirm_or_cancel("添加任务", is_confirm=False)

    # 修改任务界面中的车辆违停时限
    def update_input_park_time(self, task_name, is_confirm=True):
        # 点击编辑icon
        TableListPage(self.driver).operations_table_list(task_name, flag="edit")
        # 修改违停时限为2分钟
        self.input_park_time(2)
        # 点击确认或取消按钮
        if is_confirm:
            CONFIRM_BTN = (By.XPATH, f'//div[@aria-label="编辑"]/parent::div[not(@style="display: none;")]//span[@class="dialog-footer"]//span[text()="确定"]')
            BasePage(self.driver).click_ele(CONFIRM_BTN)
        else:
            CONFIRM_BTN = (By.XPATH,
                           f'//div[@aria-label="编辑"]/parent::div[not(@style="display: none;")]//span[@class="dialog-footer"]//span[text()="取消"]')
            BasePage(self.driver).click_ele(CONFIRM_BTN)

    # 点击左侧任务菜单
    def click_left_menu(self, menu_name):
        TASK_MENU = (By.XPATH, f'//div[@class="task-menu-container"]//li[contains(text(), "{menu_name}")]')
        BasePage(self.driver).click_ele(TASK_MENU)

    # 点击添加任务按钮
    def click_add_task_btn(self):
        ADD_BTN = (By.XPATH, '//span[contains(text(), "添加任务")]')
        BasePage(self.driver).click_ele(ADD_BTN)

    # 点击批量操作按钮
    def click_batch_operation_btn(self):
        ADD_BTN = (By.XPATH, '//span[contains(text(), "批量操作")]')
        BasePage(self.driver).click_ele(ADD_BTN)

    # 点击全选
    def check_all(self):
        ALL_SELECT = (By.XPATH, '//div[@class="el-table__header-wrapper"]//div[text()="任务名称"]/parent::th/preceding-sibling::th//span[@class="el-checkbox__input"]')
        BasePage(self.driver).wait_for_ele_to_be_visible(ALL_SELECT)
        BasePage(self.driver).click_ele(ALL_SELECT)

    # 点击返回icon，回到默认状态界面
    def click_back_icon(self):
        BTN = (By.XPATH, '//span[contains(text(), "批量删除")]/parent::button/preceding-sibling::button')
        BasePage(self.driver).click_ele(BTN)

    def crumbs_btn_opreration(self, btn_text):
        BTN = (By.XPATH, f'//span[contains(text(), "{btn_text}")]')
        BasePage(self.driver).click_ele(BTN)

    # 点击批量禁用按钮
    # def click_batch_disabled_btn(self):
    #     BTN = (By.XPATH, '//span[contains(text(), "批量禁用")]')
    #     BasePage(self.driver).click_ele(BTN)
    # 点击批量启用按钮
    # def click_batch_start_btn(self):
    #     BTN = (By.XPATH, '//span[contains(text(), "批量启用")]')
    #     BasePage(self.driver).click_ele(BTN)
    # 点击批量删除按钮
    # def click_batch_delete_btn(self):
    #     BTN = (By.XPATH, '//span[contains(text(), "批量删除")]')
    #     BasePage(self.driver).click_ele(BTN)

    # 进行任务的全批量操作。如：批量禁用、批量启用和批量删除
    def task_batch_operation(self, flag, text="确定"):
        # 点击批量操作按钮
        self.click_batch_operation_btn()
        # 全选操作
        self.check_all()
        if flag == "disabled":
            # 点击批量禁用按钮
            self.crumbs_btn_opreration(btn_text="批量禁用")
        elif flag == "start":
            # 点击批量启用按钮
            self.crumbs_btn_opreration(btn_text="批量启用")
        elif flag == "delete":
            # 点击批量删除按钮
            self.crumbs_btn_opreration(btn_text="批量删除")

            """ 针对批量 """
            # 定位批量全选不能操作的情况
            BTN = (By.XPATH,
                   '//div[@class="el-table__header-wrapper"]//div[text()="任务名称"]/parent::th/preceding-sibling::th//span[contains(@class, "el-checkbox__input") and contains(@class, "is-disabled")]')
            try:
                # 如果全选按钮处于不可点击状态，则说明当前页面的列表为空
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(BTN))
            except:
                # 删除
                pass
            else:
                # 如果定位不到，则说明有任务列表，可以进行批量删除操作
                pass

        if text == "确定":
            # dialog窗口 - 确定状态的修改
            DialogPage(self.driver).operation_dialog_btn()
        elif text == "取消":
            # dialog窗口 - 取消状态的修改
            DialogPage(self.driver).operation_dialog_btn(btn_text="取消")
        elif text == "删除":
            # dialog窗口 - 批量删除
            DialogPage(self.driver).operation_dialog_btn(btn_text="删除")

    # 验证当前页的批量任务禁用操作是否成功
    def verify_operation_disabled_success(self):
        """ 如果在页面中能定位到该元素，则批量禁用操作失败，反之成功 """
        # 在任务批量禁用之后，查看页面是否还存在启用状态的任务
        SWITCH = (By.XPATH, '//table[@class="el-table__body"]//div[@role="switch" and contains(@class, "is-checked")]')
        try:
            time.sleep(1)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(SWITCH))
        except:
            return True
        else:
            return False

    # 验证当前页面的批量任务删除操作是否成功
    def verify_operation_delete_success(self):
        # 批量删除操作之后定位tr，如果存在，则批量删除失败，反之成功
        ELE_LOC = (By.XPATH, '//table[@class="el-table__body"]//tbody//tr')
        try:
            time.sleep(1)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ELE_LOC))
        except:
            return True
        else:
            return False

    # 验证当前页的批量任务启用操作是否成功
    def verify_operation_start_success(self):
        """ 如果在页面中能定位到该元素，则批量启用操作失败，反之成功 """
        # 在任务批量启用之后，查看页面是否还存在停用状态的任务
        SWITCH = (By.XPATH, '//table[@class="el-table__body"]//div[@role="switch" and not(contains(@class, "is-checked"))]')
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(SWITCH))
        except:
            return False
        else:
            return True

    # 添加各种任务类型共用的部分
    def task_basic_set(self, task):
        # 输入任务名称
        self.input_task_name(task_name=task.task_name)
        # 通过设备名选择设备
        self.select_device(device_name=task.device_name)
        # 设置特殊属性
        # self.select_special_attr(attr_name=task.special_attributes)

    """ ---------------------------- 添加任务 - dialog界面元素操作 ---------------------------- """

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
            # if len(attr_name) > 1:
            for single_attr in attr_name:
                # 通过指定特殊属性的名称，进行选择
                # SELECT_ATTR = (By.XPATH, f'//span[text()="{attr_name}"]')
                SELECT_ATTR = (By.XPATH, f'//span[text()="{single_attr}"]')
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
        BasePage(self.driver).click_ele(RESULT)

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

    # 点击关闭任务添加窗口
    # def click_close_task_add_btn(self):
    #     # 定位关闭弹窗
    #     CLOSE_BUTTON = (By.XPATH, '//div[@class="el-dialog__wrapper"]//span[contains(text(), "添加任务")]/following-sibling::button')
    #     BasePage(self.driver).click_ele(CLOSE_BUTTON)

    # 点击关闭任务详情窗口
    # def click_close_task_view_btn(self):
    #     # 定位关闭弹窗
    #     CLOSE_BUTTON = (By.XPATH,
    #                     '//div[not(contains(@style, "display: none;")) and contains(@class, "el-dialog__wrapper")]//div[@class="el-dialog__header"]//button')
    #     BasePage(self.driver).click_ele(CLOSE_BUTTON)

    # 创建车辆任务的非空校验

    def verify_parked_vehicle_not_null(self):
        """ 点击添加任务，点击确认，进行车辆违停的非空校验"""
        # 点击左侧菜单
        self.click_left_menu("车辆-违停检测任务")
        # 点击添加任务
        self.click_add_task_btn()
        DialogPage(self.driver).is_confirm_or_cancel(loc_by_til="添加任务")

    # 创建人体区域入侵任务的非空校验
    def verify_pedestrians_not_null(self):
        """ 点击添加任务，点击确认，进行人体区域入侵的非空校验"""
        # 点击左侧菜单
        self.click_left_menu("人体-区域闯入检测任务")
        # 点击添加任务
        self.click_add_task_btn()
        DialogPage(self.driver).is_confirm_or_cancel(loc_by_til="添加任务")

    # 任务详情查看
    def verify_view_task_detail(self):
        """ 验证查看任务详情是否是当前任务名的详情 """
        TASK_NAME = (By.XPATH, '//label[contains(text(), "任务名称")]/following-sibling::div')
        time.sleep(2)
        return BasePage(self.driver).get_text(TASK_NAME)

    # 任务编辑-验证违停时限是否修改成功
    def verify_input_park_time(self, task_name):
        """ 修改任务的违停时限之后，进入详情页面，获取违停时限的文本值 """
        # 进入任务详情页
        TableListPage(self.driver).operations_table_list(task_name, flag="view")
        INPUT_PARK_TIME = (By.XPATH, '//label[contains(text(), "违停时限")]/following-sibling::div')
        result = BasePage(self.driver).get_text(INPUT_PARK_TIME)
        print(f'获取修改后的违停时限为：{result}')
        return result


if __name__ == '__main__':
    from selenium import webdriver
    from guard.pages.login_page import LoginPage
    from guard.pages.components.menubar import MenuBarPage
    from guard.pages.classes.task import Task

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://10.151.3.96/login")
    LoginPage(driver).login("zhuwenqin", "888888", login_way="debug")
    MenuBarPage(driver).click_nav_item("配置", "任务管理")

    # task = Task("wse", "3210")
    # TaskPage(driver).add_task_by_type(task, task_type="车辆-违停检测任务")
    # TaskPage(driver).add_task_to_parked_vehicle(task_name="test", device_name="1111", time_minute=1)

    # from guard.pages.components.table_list import TableListPage
    # TaskPage(driver).click_left_menu("车辆-违停检测任务")
    # TableListPage(driver).operations_table_list(name="id-2b244f07-cb55-47e7-87ef-3dca9ca47593", flag="delete")

    # TaskPage(driver).operation_batch_disabled()
