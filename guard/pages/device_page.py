# -*- coding:utf-8 -*-
# @Time: 2020/4/20 17:59
# @Author: wenqin_zhu
# @File: device_page.py
# @Software: PyCharm

import time

# 导入参数
from guard.pages.classes.rtsp import Rtsp

from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage
from guard.pages.components.dialog import DialogPage


class DevicePage(BasePage):

    def add_device_by_type(self, device, device_type, is_confirm=True):
        """
        通过指定类型来添加不同的设备
        :param device: 设备实例
        :param device_type: 设备类型，默认为网络摄像机，可选人脸识别机（后）、人脸抓拍机、身份验证一体机、人脸识别机（前）
        :param is_confirm: 是否确认，默认为确认
        """

        # 点击添加设备按钮
        self.click_add_device_btn()
        # 选择设备类型
        self.select_device_type(device_type=device_type)
        """ 开始添加设备界面的基础共用操作：设备名称、设备id、设备分组，指定地图分组，给设备标注点位 """
        self.device_basic_set(device)

        if device_type == "网络摄像机":
            # 选择camera的类型，有RTSP和ONVIF两种类型
            self.select_camera_type()
            if isinstance(device, Rtsp):
                # 输入rtsp的地址
                self.input_rtsp_address(device.rtsp_address)
                """ 编码类型和传输协议使用默认 """
            # elif isinstance(device, ONVIF):
            elif isinstance(device, Rtsp):
                pass
        elif type == "人脸识别机（前）":
            pass
        elif type == '人脸抓拍机':
            pass

        if is_confirm:
           DialogPage(self.driver).is_confirm_or_cancel("添加设备")
        else:
            DialogPage(self.driver).is_confirm_or_cancel("添加设备", is_confirm)

    # 点击添加设备
    def click_add_device_btn(self):
        ADD_BTN = (By.XPATH, '//span[contains(text(), "添加设备")]')
        BasePage(self.driver).click_ele(ADD_BTN)

    # 添加设备的共用基本参数设置
    def device_basic_set(self, device):
        # 设置设备名称
        self.input_device_name(device.device_name)
        # 设置设备id
        self.input_device_id(device.device_id)
        # 选择设备分组名称
        self.select_device_group(device.group_name)
        # 选定地图分组并在地图上标注设备的安装点位
        self.select_device_site(device.floor_name)

    """ ---------------------------- 添加设备 - dialog界面元素操作 ---------------------------- """
    # 定位-设备类型
    def select_device_type(self, device_type):

        # 定位设备类型框 并点击
        TYPE = (By.XPATH, '//label[contains(text(), "设备类型")]/following-sibling::div//input')
        # 通过传入的不同设备类型 - 去动态定位设备类型
        SELECT_TYPE = (By.XPATH,
                       f'//div[contains(@class,"el-popper") and contains(@style, "position")]//ul[contains(@class, "el-select-dropdown__list")]//span[contains(text(), "{device_type}")]')

        BasePage(self.driver).click_ele(TYPE)
        time.sleep(0.2)
        # 移动到type元素并选择目标元素
        BasePage(self.driver).mouse_move_ele_and_click(TYPE, SELECT_TYPE)

    # 定位-名称
    def input_device_name(self, name):
        NAME = (By.XPATH, '//label[contains(text(), "名称")]/following-sibling::div//input')
        BasePage(self.driver).update_input_text(NAME, name)

    # 定位-ID
    def input_device_id(self, id):
        ID = (By.XPATH, '//label[contains(text(), "ID")]/following-sibling::div//input')
        BasePage(self.driver).update_input_text(ID, id)

    # 定位-分组
    def select_device_group(self, device_group_name="Defualt", is_confirm=True):
        """ 定位到设备分组 - 并为当前创建的设备选择设备组 """

        GROUP = (By.XPATH, '//label[contains(text(), "分组")]/following-sibling::div')
        time.sleep(0.2)
        BasePage(self.driver).click_ele(GROUP)

        # 选择设备分组
        self.comm_search_result_by_name(device_group_name)
        if is_confirm:
            # 点击确定
            CONFIRM_BTN = (
                By.XPATH, '//div[@role="tooltip" and contains(@style, "position")]//span[contains(text(), "确定")]')
            BasePage(self.driver).click_ele(CONFIRM_BTN)
        else:
            # 点击取消
            CANCLE_BTN = (
                By.XPATH, '//div[@role="tooltip" and contains(@style, "position")]//span[contains(text(), "取消"]')
            BasePage(self.driver).click_ele(CANCLE_BTN)

    # 定位-地点
    def select_device_site(self, map_group_name="Default", is_confirm=True):
        """ 标准设备在地图中的点位 """

        SITE = (By.XPATH, '//label[contains(text(), "地点")]/following-sibling::div//span')
        # 点击按钮 - 在弹框界面进行设备点位标注
        BasePage(self.driver).click_ele(SITE)

        # 搜索地图设备分组，并点击搜索到的结果
        SEARCH_GROUP = (By.XPATH, '//input[contains(@placeholder, "请输入平面图名称")]')
        BasePage(self.driver).update_input_text(SEARCH_GROUP, map_group_name)
        MAP_GROUP = (By.XPATH, f'//span[contains(text(), "{map_group_name}")]')
        BasePage(self.driver).click_ele(MAP_GROUP)

        # 定位 - 地图点位图标
        MAP_POINT = (By.XPATH, '//a[contains(@title, "Draw a marker")]')
        BasePage(self.driver).click_ele(MAP_POINT)

        # 定位 - 地图容器
        TARGET_ELE = (By.XPATH, '//div[@class="leaflet-control-container"]')
        BasePage(self.driver).mouse_move_to_ele_and_offset(x_offset=100, y_offset=100, loc=TARGET_ELE)

        if is_confirm:
            # 点击确定
            CONFIRM_BTN = (
                By.XPATH, '//div[contains(@class, "dialog-track")]//span[contains(text(), "确定")]')
            BasePage(self.driver).click_ele(CONFIRM_BTN)
        else:
            # 点击取消
            CANCLE_BTN = (
                By.XPATH, '//div[contains(@class, "dialog-track")]//span[contains(text(), "取消")]')
            BasePage(self.driver).click_ele(CANCLE_BTN)

    # 定位-分配用户：设置设备分配给哪些用户
    def assign_device_jurisdiction_to_user(self):
        DEVICE_JUR = (By.XPATH, '//label[contains(text(), "分配用户")]/following-sibling::div//input')
        BasePage(self.driver).click_ele(DEVICE_JUR)

    """ ---------------------------- 设备类型 - 网络摄像机 - 类型为：RTSP ---------------------------- """
    # 定位-类型<RTSP/ONVIF>
    def select_camera_type(self, camera_type="RTSP"):
        TYPE = (By.XPATH, f'//div[@class="el-form-item__content"]//span[contains(text(), "{camera_type}")]')
        # 点击选择 - 摄像机类型
        BasePage(self.driver).click_ele(TYPE)

    # 定位-RTSP地址
    def input_rtsp_address(self, rtsp_address):
        ADDRESS = (By.XPATH, '//label[contains(text(), "RTSP地址")]/following-sibling::div//input')
        BasePage(self.driver).update_input_text(ADDRESS, rtsp_address)

    # 定位-RTSP地址-右侧的预览视频icon
    def view_rtsp_video(self):
        VIEW = (By.XPATH, '//label[contains(text(), "RTSP地址")]/following-sibling::div/i')
        # 点击ICON图标 - 进行RTSP地址的视频预览
        BasePage(self.driver).click_ele(VIEW)

    # 定位-编码类型<直连/转码>
    def select_encoding_type(self, default="直连"):
        TYPE = (By.XPATH, f'//div[@class="el-form-item__content"]//span[contains(text(), "{default}")]')
        # 点击选择编码类型
        BasePage(self.driver).click_ele(TYPE)

    # 定位-传输协议<TCP/UDP>
    def select_transport_protocols(self, default="TCP"):
        PROTOCOLS = (By.XPATH, f'//div[@class="el-form-item__content"]//span[contains(text(), "{default}")]')
        BasePage(self.driver).click_ele(PROTOCOLS)

    # 定位-将该设备关联门禁开关
    def is_open_switch(self, is_open=False):
        BTN = (By.XPATH, '//label[contains(text(), "将该设备关联门禁开关")]/following-sibling::div//div[@role="switch"]')
        # 点击确认是否设置该设备关联门禁开关 - 默认不关联
        if is_open:
            BasePage(self.driver).click_ele(BTN)

    """ ---------------------------- 页面共用封装方法 ---------------------------- """
    def comm_search_result_by_name(self, name):
        """ 下拉列表搜索 """
        # 1、通过设备分组名device_group_name,查找设备
        SELECT_GROUP = (By.XPATH,
                        '//div[@role="tooltip" and contains(@style, "position")]//div[contains(@class, "el-input--small")]//input')
        BasePage(self.driver).update_input_text(SELECT_GROUP, name)

        # 2、通过设备分组名device_group_name, 定位到查询结果
        RESULT = (By.XPATH, f'//span[@class="el-radio__label" and text() = "{name}"]')
        # 点击到查询的设备分组名
        BasePage(self.driver).click_ele(RESULT)


if __name__ == '__main__':
    from selenium import webdriver
    from guard.pages.login_page import LoginPage
    from guard.pages.components.menubar import MenuBarPage

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://10.151.3.96/login")
    LoginPage(driver).login("zhuwenqin", "888888", login_way="debug")
    MenuBarPage(driver).click_nav_item("配置", "设备管理")
    device = Rtsp("a", "111", "Default", "Default", "rtsp://10.151.3.119:7554/IMG_0322.264")
    DevicePage(driver).add_device_by_type(device, device_type="网络摄像机")

