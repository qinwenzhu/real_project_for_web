# -*- coding:utf-8 -*-
# @Time: 2020/4/29 16:01
# @Author: wenqin_zhu
# @File: dialog.py
# @Software: PyCharm

from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage

""" 
全局组件 - dialog对话弹框操作

如：创建同级/下一级分组，…… 
"""


class DialogPage(BasePage):

    # 通过dialog对话框的标题名，创建group分组
    def create_group_by_dialog_title_name(self, loc_by_til, group_name, is_confirm=True, **kwargs):
        # 组名称input框
        GROUP_INPUT = (By.XPATH, f'//span[contains(text(),"{loc_by_til}")]/parent::div/following-sibling::div[@class="el-dialog__body"]//input')
        BasePage(self.driver).update_input_text(GROUP_INPUT, group_name)

        self.is_confirm_or_cancel(loc_by_til, is_confirm)

    # dialog对话框的确定或取消操作
    def is_confirm_or_cancel(self, loc_by_til, is_confirm=True):
        if is_confirm:
            # 定位确认按钮
            CONFIRM_BTN = (By.XPATH, f'//span[contains(text(),"{loc_by_til}")]/parent::div/following-sibling::div[@class="el-dialog__footer"]//span[contains(text(),"确定")]')
            BasePage(self.driver).click_ele(CONFIRM_BTN)
        else:
            # 定位取消按钮
            CANCLE_BTN = (By.XPATH, f'//span[contains(text(),"{loc_by_til}")]/parent::div/following-sibling::div[@class="el-dialog__footer"]//span[contains(text(),"取消")]')
            BasePage(self.driver).click_ele(CANCLE_BTN)

    # dialog对话框的删除或取消操作
    def is_delete_or_cancel(self, index=None, is_delete=True):

        if is_delete:
            # 点击删除按钮
            DELETE_BTN = (By.XPATH, '//button//span[contains(text(), "删除")]')
            # 返回元素
            ele = BasePage(self.driver).get_ele_locator_by_index(DELETE_BTN, index)
            # 点击按钮
            ele.click()
            # BasePage(self.driver).click_ele(DELETE_BTN)
        else:
            # 点击取消按钮
            CANCLE_BTN = (By.XPATH, '//button//span[contains(text(), "取消")]')
            BasePage(self.driver).click_ele(CANCLE_BTN)
