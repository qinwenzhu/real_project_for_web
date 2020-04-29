# -*- coding:utf-8 -*-
# @Time: 2020/3/30 18:52
# @Author: wenqin_zhu
# @File: user_page.py
# @Software: PyCharm

import time
from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage
from guard.pages.components.group_tree import GroupTreePage


class UserPage(BasePage):

    def add_user(self):
        # 添加用户
        pass


if __name__ == '__main__':
    from selenium import webdriver
    from guard.pages.components.menubar import MenubarPage
    from guard.pages.login_page import LoginPage
    driver = webdriver.Chrome()
    driver.get("http://10.151.3.96/login")
    LoginPage(driver).login("zhuwenqin", "888888", login_way="ssh")
    MenubarPage(driver).click_nav_item("配置", "用户管理")
