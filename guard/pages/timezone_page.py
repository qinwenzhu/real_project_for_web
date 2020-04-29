# -*- coding:utf-8 -*-
# @Time: 2020/4/10 16:09
# @Author: wenqin_zhu
# @File: timezone_page.py
# @Software: PyCharm

import time
from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage
from guard.pages.classes.web_global_dialog import GlobalDialog


class TimezonePage(BasePage):

    def add_timezone(self, timezone_name):
        """
        添加时间条件
        :param timezone_name: 填入时间条件的名称
        """

        # icon的识别率不高，添加强制等待提高用例成功率
        time.sleep(2)
        # 定位 -添加时间条件- 的按钮icon
        ICON = (By.XPATH, '//span[contains(text(), "时间条件名称")]/i')
        BasePage(self.driver).click_ele(ICON)
        # 调用封装方法 - 添加时间条件名称
        self.dialog_info_com("添加时间条件", timezone_name)

    def add_timezone_section_by_timezone_name(self, timezone_name):
        """
        添加时间段
        :param timezone_name: 给传入的timezone添加时间段
        """

        # 定位到传入的timezone时间条件
        SELECT_TIMEZONE = (By.XPATH, f'//div[@role="tablist"]//button/span[contains(text(), "{timezone_name}")]')
        # 定位到 -时间段- 的按钮icon
        ICON = (By.XPATH, '//span[contains(text(), "时间段")]/i')
        if not self.driver.find_element(*SELECT_TIMEZONE).is_displayed():
            time.sleep(0.5)
            # 元素滚动到页面可见区域
            BasePage(self.driver).scroll_visibility_region(loc=SELECT_TIMEZONE)
        # 点击元素
        BasePage(self.driver).click_ele(SELECT_TIMEZONE)
        # 点击添加时间段
        time.sleep(0.5)
        BasePage(self.driver).click_ele(ICON)

    def create_holidays(self, tile_name, holidays, num=0):
        """
        添加假期
        :param tile_name: 动态传入定位表达式的标题名称
        :param holidays: 假期名称
        :param num: 设置动态数值，保证时间选择不同
        """
        # 定位 - 未定义假期 - 按钮
        SET_HOLIDAY = (By.XPATH, '//span[contains(text(), "未定义假期")]')
        if not self.driver.find_element(*SET_HOLIDAY).is_displayed():
            # 元素滚动到页面可见区域
            BasePage(self.driver).scroll_visibility_region(loc=SET_HOLIDAY)
        # 点击 - 未定义假期 - 按钮
        BasePage(self.driver).click_ele(SET_HOLIDAY)
        # 调用封装方法 - 添加假期
        self.dialog_info_com(tile_name, holidays)

        # 点击 - 设定日期 - 按钮
        SET_TIME = (By.XPATH, '//header[contains(text(), "假期定义")]/following-sibling::div//span[contains(text(), "设定日期")]')
        BasePage(self.driver).click_ele(SET_TIME)
        # 调用封装方法 - 选择假期的时间区间
        self.check_time(num)

    def create_workday(self, tile_name, val, num=0):
        """
        添加特殊工作日
        :param tile_name: 动态传入定位表达式的标题名称
        :param val: 特殊工作日名称
        :param num: 设置动态数值，保证时间选择不同
        """

        # 定位 - 未定义工作日 - 按钮
        SET_WORKDAY = (By.XPATH, '//span[contains(text(), "未定义工作日")]')
        if not self.driver.find_element(*SET_WORKDAY).is_displayed():
            # TODO 判断元素在页面是否可见 ele.is_displayed()，默认可见
            # 元素滚动到页面可见区域
            BasePage(self.driver).scroll_visibility_region(loc=SET_WORKDAY)
        # 点击 - 未定义工作日 - 按钮
        BasePage(self.driver).click_ele(SET_WORKDAY)
        # 调用封装方法 - 添加特殊工作日
        self.dialog_info_com(tile_name, val)

        # 点击 - 设定日期 - 按钮
        SET_TIME = (By.XPATH, '//header[contains(text(), "特殊工作日定义")]/following-sibling::div//span[contains(text(), "设定日期")]')
        BasePage(self.driver).click_ele(SET_TIME)
        # 调用封装方法 - 选择特殊工作日的时间区间
        self.check_time(num)

    def delete_or_rename_timezone_name(self, timezone_name, is_delete="删除"):
        """ 删除时间条件 """

        # 定位到当前时间条件名称
        SELECT_TIMEZONE = (By.XPATH, f'//div[@role="tablist"]//button/span[contains(text(), "{timezone_name}")]')
        BasePage(self.driver).mouse_move_ele(SELECT_TIMEZONE)
        if is_delete == "重命名":
            # TODO
            # 定位到 "重命名" 元素
            ELE_LOC = (By.XPATH,
                       '//div[@role="tooltip"  and contains(@style, "position")]//span[contains(text(), "重命名")]')
            BasePage(self.driver).mouse_move_ele_and_click(SELECT_TIMEZONE, ELE_LOC)
            # 执行重命名操作
            self.dialog_info_com("重命名时间条件", "UPDATE" + timezone_name)

        elif is_delete == "删除":
            # 定位到 "删除" 元素
            ELE_LOC = (By.XPATH,
                       '//div[@role="tooltip"  and contains(@style, "position")]//span[contains(text(), "删除")]')
            BasePage(self.driver).mouse_move_ele_and_click(SELECT_TIMEZONE, ELE_LOC)
            # 执行删除操作
            GlobalDialog(self.driver).dialog_delete()

    def delete_or_rename_holidays_or_workday(self, timezone_name, is_delete="删除"):
        """ 删除假期或特殊工作日 """

        # 定位到当前假期或特殊工作日
        SELECT_TIMEZONE = (By.XPATH, f'//span[text()="{timezone_name}"]/ancestor::tr')
        BasePage(self.driver).mouse_move_ele(SELECT_TIMEZONE)
        if is_delete == "重命名":
            # TODO
            # 定位到 "重命名" 元素
            ELE_LOC = (By.XPATH,'//div[@class="timezone-left-popper"]//span[contains(text(), "重命名")]')
        elif is_delete == "删除":
            # 定位到 "删除" 元素
            ELE_LOC = (By.XPATH,
                       '//div[@class="timezone-left-popper"]//span[contains(text(), "删除")]')
            BasePage(self.driver).mouse_move_ele_and_click(SELECT_TIMEZONE, ELE_LOC)
            # 执行删除操作
            GlobalDialog(self.driver).dialog_delete()

    def dialog_info_com(self, til_name, val, confirm=True):
        """
        封装dialog弹框
        :param til_name: 弹框标题
        :param val: 传入input输入框值
        :param confirm: dialog按钮选项。默认确定
        """

        INPUT_TEXT = (By.XPATH, f'//div[@class="timezone-rename-dialog-header"]//span[contains(text(), "{til_name}")]/ancestor::div[@class="el-dialog__header"]/following-sibling::div[@class="el-dialog__body"]//input')
        BasePage(self.driver).update_input_text(INPUT_TEXT, val)
        if confirm:
            CONFIRM_BUTTON = (By.XPATH,
                              f'//div[@class="timezone-rename-dialog-header"]//span[contains(text(), "{til_name}")]/ancestor::div[@class="el-dialog__header"]/following-sibling::div[@class="el-dialog__footer"]//span[contains(text(), "确定")]')
            BasePage(self.driver).click_ele(CONFIRM_BUTTON)
        else:
            CANCEL_BUTTON = (By.XPATH,
                             f'//div[@class="timezone-rename-dialog-header"]//span[contains(text(), "{til_name}")]/ancestor::div[@class="el-dialog__header"]/following-sibling::div[@class="el-dialog__footer"]//span[contains(text(), "取消")]')
            BasePage(self.driver).click_ele(CANCEL_BUTTON)

    def check_time(self, num=1):
        """ 封装时间控件 """

        # 定位到时间控件并通过鼠标操作
        TIME_CONTROL = (By.XPATH, '//div[contains(@class, "el-date-range-picker") and contains(@style, "position")]//td[contains(@class, "today")]')
        BasePage(self.driver).mouse_move_ele(TIME_CONTROL)

        # 滑动时间控件点击对应的日期
        TIME_TODAY = (By.XPATH, '//div[contains(@class, "el-date-range-picker") and contains(@style, "position")]//div[contains(@class,"is-left")]//td[contains(@class, "today")]')
        BasePage(self.driver).mouse_move_ele_and_click(TIME_CONTROL, TIME_TODAY)

        TODAY_TEXT = (By.XPATH, '//div[contains(@class, "el-date-range-picker") and contains(@style, "position")]//div[contains(@class,"is-left")]//td[contains(@class, "today")]//span')
        today_text = BasePage(self.driver).get_text(TODAY_TEXT)
        if int(today_text) >= 28:
            # 结束时间为下月1号
            today_text = "1"
            TIME_END = (By.XPATH, f'//div[contains(@class, "el-date-range-picker") and contains(@style, "position")]//div[contains(@class,"is-right")]//td//span[contains(text(),{today_text})]')
        else:
            # 结束时间为今天的后两天
            today_text = str(int(today_text)+num)
            # 默认选择时间段为全天24小时
            TIME_END = (By.XPATH, f'//div[contains(@class, "el-date-range-picker") and contains(@style, "position")]//div[contains(@class,"is-left")]//td//span[contains(text(),{today_text})]')
        BasePage(self.driver).mouse_move_ele_and_click(TIME_CONTROL, TIME_END)

    def assert_result_by_name(self, name):
        # 判断添加操作是否成功，包括：时间条件、假期、特殊工作日
        RESULT = (By.XPATH, f'//span[contains(text(), "{name}")]')
        return BasePage(self.driver).get_text(RESULT)

    def assert_timezone_section(self):
        # 判断添加时间段是否成功
        CHECK_CON_RESULT = (By.XPATH, '//div[@class="el-tab-pane" and @style=""]//div[contains(@class, "el-row")]//span[contains(text(), ":")]')
        return BasePage(self.driver).get_text(CHECK_CON_RESULT)


if __name__ == '__main__':
    from selenium import webdriver
    from guard.pages.components.menubar import MenubarPage
    from guard.pages.login_page import LoginPage
    driver = webdriver.Chrome()
    driver.get("http://10.151.3.96/login")
    LoginPage(driver).login("zhuwenqin", "888888", login_way="ssh")
    MenubarPage(driver).click_nav_item("配置", "时间条件")
    TimezonePage(driver).add_timezone("test_时间条件")
    # TimezonePage(driver).create_holidays("添加假期", "假期名称1")
    # TimezonePage(driver).create_workday("添加特殊工作日", "工作日名称1")
    # TimezonePage(driver).add_timezone_name("timezone1")
    # TimezonePage(driver).add_timezone_name("timezone2")
    # TimezonePage(driver).delete_or_rename_timezone_name("timezone1", "重命名")
    # TimezonePage(driver).delete_or_rename_timezone_name("timezone2", "删除")
