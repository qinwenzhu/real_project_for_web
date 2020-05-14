# -*- coding:utf-8 -*-
# @Time: 2020/5/13 11:05
# @Author: wenqin_zhu
# @File: record_page.py
# @Software: PyCharm

import time
from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage
from guard.pages.components.dialog import DialogPage
from selenium.webdriver.support.wait import WebDriverWait
from guard.pages.components.table_list import TableListPage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class RecordPage(BasePage):

    # 点击车辆记录
    def click_tab_list_btn(self):
        TAB_ID = (By.ID, "tab-vehicle")
        BasePage(self.driver).click_ele(TAB_ID)

    # 点击筛选按钮
    def click_filter_btn(self):
        BTN = (By.XPATH, '//div[@class="main-container"]//div[@class="filtrate-nav"]//span[contains(text(), "筛选") and contains(@class, "screen")]')
        BasePage(self.driver).click_ele(BTN)

    # 进行过滤项的属性选择 - 设备
    def filter_device(self):
        BTN = (By.XPATH, '//div[@class="condition-box"]//div[contains(@class, "tree-input")]//span[contains(text(), "设备")]')
        BasePage(self.driver).click_ele(BTN)

    """  任务下拉列表搜索 """
    def comm_search_result_by_name(self, name):
        # 点击出现下拉选择搜索框
        CLICK_BTN = (By.XPATH, '//div[@class="condition-box"]//div[contains(@class, "tree-input")]//span[contains(text(), "设备")]/following-sibling::div')
        BasePage(self.driver).click_ele(CLICK_BTN)
        # 强制等待3秒，等下拉列表全部加载完成，再进行搜索查询
        time.sleep(3)
        # 通过设备名device_name,查找设备
        SELECT_GROUP = (By.XPATH,
                        '//ul[contains(@class, "el-dropdown-menu") and not(contains(@style, "display: none;"))]//div[contains(@class, "el-input")]//input')
        BasePage(self.driver).update_input_text(SELECT_GROUP, name)
        # 通过 name, 定位到查询结果
        RESULT = (By.XPATH, f'//ul[contains(@class, "el-dropdown-menu") and not(contains(@style, "display: none;"))]//div[@class="el-tree-node__content"]//span[text()="{name}"]/preceding-sibling::span/following-sibling::label')
        # 点击查询到的name
        BasePage(self.driver).click_ele(RESULT)

    # 点击筛选或重置按钮
    def click_filter_or_reset_btn(self, default="filter"):
        if default == "filter":
            BTN = (By.XPATH, '//div[@class="condition-box"]//div[@class="operate"]//span[contains(text(), "筛选")]')
            # 点击筛选
            BasePage(self.driver).click_ele(BTN)
        else:
            BTN = (By.XPATH, '//div[@class="condition-box"]//div[@class="operate"]//span[contains(text(), "重置")]')
            # 点击重置
            BasePage(self.driver).click_ele(BTN)

    # 验证当前设备绑定的任务是否有记录产生
    def get_record_total(self):
        # 定位到搜索到的记录条数
        COUNT = (By.XPATH, '//div[@class="block"]//span[@class="el-pagination__total"]')
        data = BasePage(self.driver).get_text(COUNT)
        count = ""
        if isinstance(data, str):
            for i in data:
                if i.isdigit():
                    count += i
            return int(count)
        else:
            print("内容错误！")

    # 验证记录推送的条数是否大于0
    def verify_record_total(self):
        try:
            data = self.get_record_total()
            print(f"当前任务的记录推送总条数为：{data}")
            if data > 0:
                return True
        except:
            return False

    # 通过设备进行记录的筛选
    def record_filter_by_device(self, device_name):
        """
        通过设备名称进行记录的筛选
        :param device_name:
        :return:
        """
        # 点击车辆记录
        self.click_tab_list_btn()
        # 点击筛选按钮
        self.click_filter_btn()
        # 根据设备名称进行筛选过滤
        self.comm_search_result_by_name(device_name)
        # 点击筛选按钮
        self.click_filter_or_reset_btn()


if __name__ == '__main__':
    from selenium import webdriver
    from guard.pages.login_page import LoginPage
    from guard.pages.components.menubar import MenuBarPage

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://10.151.3.96/login")
    LoginPage(driver).login("zhuwenqin", "888888", login_way="debug")
    MenuBarPage(driver).click_nav_item("记录")
    RecordPage(driver).click_tab_list_btn()
    RecordPage(driver).click_filter_btn()
    RecordPage(driver).comm_search_result_by_name(name="3210")
    RecordPage(driver).click_filter_or_reset_btn()
