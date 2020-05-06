# -*- coding:utf-8 -*-
# @Time: 2020/4/20 17:59
# @Author: wenqin_zhu
# @File: map_page.py
# @Software: PyCharm

from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage
from selenium.webdriver.support.wait import WebDriverWait
from guard.pages.components.group_tree import GroupTreePage
from selenium.webdriver.support import expected_conditions as EC


class MapPage(BasePage):

    # 上传地图
    def upload_map(self, file_name, group_name="Default"):
        # 定位上传元素
        UPLOAD_FILE = (By.XPATH, '//input[@class="el-upload__input"]')
        # 点击指定地图分组，默认点击Default分组
        GroupTreePage(self.driver).click_group_by_name(group_name)
        BasePage(self.driver).upload_file(loc=UPLOAD_FILE, filename=file_name)

    # 判断地图是否上传成功
    def is_upload_map_success(self):
        try:
            TAG = (By.XPATH, '//div[@class="main_head"]//div')
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(TAG))
        except:
            print("-------------地图上传失败/当前地图分组下没有上传地图---------------")
            return False
        else:
            return True

    # 判断地图上是否存在设备
    def map_is_exist_device(self):
        # 定位设备点位容器内的icon，如果存在<返回True>，则说明Default分组下存在设备
        try:
            DEVICE_ICON = (By.XPATH, '//div[@class="leaflet-pane leaflet-marker-pane"]//img')
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(DEVICE_ICON))
        except:
            return False
        else:
            return True


if __name__ == '__main__':
    from selenium import webdriver
    from guard.pages.login_page import LoginPage
    from guard.pages.components.menubar import MenubarPage
    driver = webdriver.Chrome()
    driver.get("http://10.151.3.96/login")
    LoginPage(driver).login("zhuwenqin", "888888", login_way="debug")
    MenubarPage(driver).click_nav_item("配置", "地图管理")
