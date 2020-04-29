# -*- coding:utf-8 -*-
# @Time: 2020/4/20 17:59
# @Author: wenqin_zhu
# @File: device_page.py
# @Software: PyCharm

import time
from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage
# from selenium.webdriver.common.action_chains import ActionChains
from guard.pages.classes.web_com_content_click import WebContentClick as click_btn


class DevicePage(BasePage):

    def add_device_com(self):
        # 点击添加设备
        ADD_BTN = (By.XPATH, '//span[contains(text(), "添加设备")]')
        BasePage(self.driver).click_ele(ADD_BTN)

    def is_confirm_or_cancel_com(self, is_confirm=True):
        if is_confirm:
            # 定位-确定按钮
            CONFIRM_BTN = (By.XPATH,
                           '//div[@class="deviceAdd"]//div[@class="el-dialog__footer"]//span[contains(text(), "确定")]')
            BasePage(self.driver).click_ele(CONFIRM_BTN)
        else:
            # 定位-取消按钮
            CANCEL_BTN = (
                By.XPATH, '//div[@class="deviceAdd"]//div[@class="el-dialog__footer"]//span[contains(text(), "取消")]')
            BasePage(self.driver).click_ele(CANCEL_BTN)

    def add_camera(self, device_type, device_name, device_id, device_group_name, map_group_name,
                   rtsp_address, camera_type="RTSP", is_confirm=True):
        """
        添加设备,设备类型为 摄像头Cam
        :param device_name: 设备名称
        :param device_id: 设备id
        :param device_group_name: 设备分组名称
        :param map_group_name: 地图分组名称
        :param rtsp_address: RTSP视频流地址
        :param camera_type: 摄像机类型划分：RTSP和ONVIF
        :param device_type: 指定创建设备的设备类型，设备类型包括<网络摄像机、人脸识别机（后）、人脸抓拍机、身份验证一体机、人脸识别机（前）>
        :param is_confirm: 确定或取消
        """

        # 添加设备
        click_btn(self.driver).click_btn(btn_name="添加设备")

        # 设置设备类型 - 网络摄像机
        self.select_device_type(device_type)
        # 设置设备名称
        self.input_device_name(device_name)
        # 设置设备id
        self.input_device_id(device_id)
        # 设置设备分组名称
        self.select_device_group(device_group_name)
        # 标注设备在地图上的点位 - <前置：需要创建地图分组，上传地图》
        self.select_device_site(map_group_name)
        # TODO 暂时使用默认
        #  设置该设备的使用权限，分配给哪些用户，自动化设置，使用默认值
        # self.assign_device_jurisdiction_to_user()
        if camera_type == "RTSP":
            # 创建摄像机类型为：RTSP 的设备
            self.camera_type_to_rtsp(rtsp_address)
        elif camera_type == "ONVIF":
            # TODO 创建摄像机类型为：ONVIF  的设备
            pass
        # TODO 是否设置该设备 - 关联无感门禁
        # self.is_open_switch(is_relevance)
        # 调用确认or取消
        self.is_confirm_or_cancel_com(is_confirm)

    def camera_type_to_rtsp(self, rtsp_address, camera_type="RTSP", encod_type="直连", tran_pro="TCP"):
        """ 设置摄像机类型为RTSP """
        # 选择类型为RTSP
        self.select_camera_type(camera_type)
        # 设置RTSP地址
        self.input_rtsp_address(rtsp_address)
        # 设置编码类型
        self.select_encoding_type(encod_type)
        # 选择传输协议
        self.select_transport_protocols(tran_pro)

    """ ---------------------------- 添加设备 - page界面操作 ---------------------------- """
    # 定位-设备类型
    def select_device_type(self, default="网络摄像机"):
        # 定位设备类型框 并点击
        TYPE = (By.XPATH, '//label[contains(text(), "设备类型")]/following-sibling::div//input')
        BasePage(self.driver).click_ele(TYPE)

        time.sleep(0.2)
        # 通过传入的不同设备类型 - 去动态定位设备类型
        SELECT_TYPE = (By.XPATH, f'//div[contains(@class,"el-popper") and contains(@style, "position")]//ul[contains(@class, "el-select-dropdown__list")]//span[contains(text(), "{default}")]')
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
        BasePage(self.driver).mouse_move_to_ele_and_offset(100, 100, loc=TARGET_ELE)

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
    def select_camera_type(self, default="RTSP"):
        TYPE = (By.XPATH, f'//div[@class="el-form-item__content"]//span[contains(text(), "{default}")]')
        # 点击选择 - 摄像机类型
        BasePage(self.driver).click_ele(TYPE)
        # 选择不同的Camera类型，进行不同的操作
        if default == "RTSP":
            pass
        elif default == "ONVIF":
            pass

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
    from guard.pages.components.menubar import MenubarPage

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://10.151.3.96/login")
    LoginPage(driver).login("zhuwenqin", "888888", login_way="debug")
    MenubarPage(driver).click_nav_item("配置", "设备管理")
    DevicePage(driver).add_camera(device_type="网络摄像机", device_name="test", device_id="test1", device_group_name="Default",
                                  map_group_name="Default", rtsp_address="rtsp://10.151.3.119:7554/IMG_0322.264")

