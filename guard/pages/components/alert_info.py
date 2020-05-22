# -*- coding:utf-8 -*-
# @Time: 2020/4/29 16:07
# @Author: wenqin_zhu
# @File: alert_info.py
# @Software: PyCharm

import logging
from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

""" 
全局组件 - alert消息框

如：添加用户成功，…… 
"""


class AlertInfoPage(BasePage):

    # 获取系统页面中的alert弹框信息
    def get_alert_info(self):

        try:
            # 定位alert弹框
            INFO_TEXT = (By.XPATH, '//div[@role="alert"]//p')
            WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(INFO_TEXT))
        except:
            self.log.debug("-------------等待alert弹框消息可见失败！---------------")
        else:
            return BasePage(self.driver).get_text(INFO_TEXT)

    # 关闭alert弹框
    def close_alert(self):

        try:
            # 定位alert弹框中的关闭按钮
            CLOSE_BTN = (By.XPATH, '//div[@role="alert"]//i[contains(@class, "el-icon-close")]')
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(CLOSE_BTN))
        except:
            self.log.debug("-------------等待alert消息弹框关闭按钮可见失败！---------------")
        else:
            BasePage(self.driver).click_ele(CLOSE_BTN)
