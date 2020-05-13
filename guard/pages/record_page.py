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
        BTN = (By.XPATH, '//div[@class="filter-condition"]//span[@class="condition-title"]')
        BasePage(self.driver).click_ele(BTN)

    # 进行过滤项的属性选择


