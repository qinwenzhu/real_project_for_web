# -*- coding: utf-8 -*-
# @time: 2020/4/19 13:11 
# @Author: wenqinzhu
# @Email: zhuwenqin_vendor@sensetime.com
# @file: web_global_dialog.py
# @software: PyCharm

from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage


class GlobalDialog(BasePage):
    """ 封装类：系统dialog弹框操作 """

    """ group_tree 弹框顶部的关闭弹窗按钮 """
    def close_dialog_btn(self, til_name):
        CLOSE_BTN = (By.XPATH, f'//span[contains(text(), "{til_name}")]/parent::div//button')
        BasePage(self.driver).click_ele(CLOSE_BTN)

    """ 通用：系统页面删除dialog """
    def dialog_delete(self, is_delete=True):

        if is_delete:
            # 点击删除按钮
            CONFIRM_BTN = (By.XPATH, '//button//span[contains(text(), "删除")]')
            BasePage(self.driver).click_ele(CONFIRM_BTN)
        else:
            # 点击取消按钮
            CONFIRM_BTN = (By.XPATH, '//button//span[contains(text(), "取消")]')
            BasePage(self.driver).click_ele(CONFIRM_BTN)

    """ 通用：系统页面提示dialog """
    def dialog_warning(self, is_confirm=True):

        if is_confirm:
            WARN_BTN = (By.XPATH, '//span[contains(text(), "提示")]/ancestor::div[@class="el-dialog__header"]/following-sibling::div[@class="el-dialog__footer"]//button//span[contains(text(), "确定")] ')
        else:
            CANCLE_BTN = (By.XPATH, '//span[contains(text(), "提示")]/ancestor::div[@class="el-dialog__header"]/following-sibling::div[@class="el-dialog__footer"]//button//span[contains(text(), "取消")] ')
