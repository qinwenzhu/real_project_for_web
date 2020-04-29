# -*- coding:utf-8 -*-
# @Time: 2020/4/27 11:10
# @Author: wenqin_zhu
# @File: web_com_content_click.py
# @Software: PyCharm


from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage


class WebContentClick(BasePage):
    """ 封装类：主体内容的按钮操作"""

    # 点击操作，如：点击添加设备、添加任务
    def click_btn(self, btn_name):
        # 点击添加设备
        # ADD_BTN = (By.XPATH, '//span[contains(text(), "添加设备")]')
        ADD_BTN = (By.XPATH, f'//span[contains(text(), "{btn_name}")]')
        BasePage(self.driver).click_ele(ADD_BTN)






