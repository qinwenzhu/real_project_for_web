# -*- coding:utf-8 -*-
# @Time: 2020/4/20 17:59
# @Author: wenqin_zhu
# @File: map_page.py
# @Software: PyCharm

import time
from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage
from selenium.webdriver.support.wait import WebDriverWait
from guard.pages.components.group_tree import GroupTreePage
from selenium.webdriver.support import expected_conditions as EC


class MapPage(BasePage):

    def upload_map(self, file_name, group_name):
        """ 地图上传 """
        # 点击指定地图分组
        GroupTreePage(self.driver).click_group_by_name(group_name)
        # 地图上传
        UPLOAD_FILE = (By.XPATH, '//input[@class="el-upload__input"]')
        BasePage(self.driver).upload_file(loc=UPLOAD_FILE, filename=file_name)
        # 等待3秒查看地图上传效果
        time.sleep(3)

    def is_upload_map_success(self):
        # 判断地图是否上传成功

        try:
            TAG = (By.XPATH, '//div[@class="main_head"]//div')
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(TAG))
        except:
            print("-------------地图上传失败！---------------")
            return False
        else:
            return True


if __name__ == '__main__':
    from selenium import webdriver
    from guard.pages.login_page import LoginPage
    from guard.pages.components.menubar import MenubarPage
    driver = webdriver.Chrome()
    driver.get("http://10.151.3.96/login")
    LoginPage(driver).login("zhuwenqin", "888888")
    MenubarPage(driver).click_nav_item("配置", "地图管理")
