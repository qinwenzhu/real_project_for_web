# -*- coding:utf-8 -*-
# @Time: 2020/4/13 19:48
# @Author: wenqin_zhu
# @File: global_dialog.py
# @Software: PyCharm

from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage


class GlobalDialogInfo(BasePage):
    """ 封装类：系统页面消息弹框
    如：添加用户成功
    """

    def judge_alert_info(self):
        """ 获取系统操作的提示消息 """

        # 定位alert弹框的文本
        INFO_TEXT = (By.XPATH, '//div[@role="alert"]//p')
        BasePage(self.driver).wait_for_ele_to_be_visible(INFO_TEXT)         # 强制等待元素可见
        return BasePage(self.driver).get_text(INFO_TEXT)

    def close_alert(self):
        """ 关闭提示消息alert弹框 """

        # 关闭alert弹框
        CLOSE_BTN = (By.XPATH, '//div[@role="alert"]//i[contains(@class, "el-icon-close")]')
        BasePage(self.driver).click_ele(CLOSE_BTN)
