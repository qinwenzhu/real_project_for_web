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

    def close_dialog(self):
        """ 关闭dialog弹框 """
        CLOSE_BTN = (By.XPATH, f'//div[not(contains(@style, "display: none;")) and contains(@class, "el-dialog__wrapper")]//div[@class="el-dialog__header"]//button')
        BasePage(self.driver).click_ele(CLOSE_BTN)

    def operation_dialog_btn(self, btn_text="确定"):
        """ 封装dialog的按钮操作
            定位到当前活动的dialog窗口，并通过传递btn的文本来动态点击按钮
         """
        BUTTON = (By.XPATH, f'//div[not(contains(@style, "display: none;")) and contains(@class, "el-dialog__wrapper")]//div[@class="el-dialog__footer"]//button//span[text()="{btn_text}"]')
        BasePage(self.driver).click_ele(BUTTON)

    # dialog对话框的确定或取消操作
    def is_confirm_or_cancel(self, loc_by_til, is_confirm=True):
        if is_confirm:
            # 定位确认按钮
            CONFIRM_BTN = (By.XPATH, f'//span[contains(text(),"{loc_by_til}")]/parent::div/following-sibling::div[@class="el-dialog__footer"]//span[contains(text(),"确定")]')
            BasePage(self.driver).click_ele(CONFIRM_BTN)
        else:
            # 定位取消按钮
            CANCLE_BTN = (By.XPATH,
                           f'//span[contains(text(),"{loc_by_til}")]/parent::div/following-sibling::div[@class="el-dialog__footer"]//span[contains(text(),"取消")]')
            # CANCLE_BTN = (By.XPATH, f'//div[@aria-label="{loc_by_til}"]/parent::div[not(@style="display: none;")]//span[@class="dialog-footer"]//span[text()="取消"]')
            BasePage(self.driver).click_ele(CANCLE_BTN)

    # dialog对话框的删除或取消操作
    def is_delete_or_cancel(self, module_val, is_delete=True):
        """
        弹框删除操作
        :param module_val: 不同模块共用，由于元素定位不一样，需要动态传入删除操作的模块
        :param is_delete:
        :return:
        """
        # 如果是用户模块的删除操作
        if module_val == "user" or module_val == "device":
            # 定位删除按钮
            DELETE_BTN = (By.XPATH,
                           '//span[contains(text(),"删除")]/parent::div/following-sibling::div[@class="el-dialog__footer"]//span[contains(text(),"删除")]')
            # 定位取消按钮
            CANCEL_BTN = (By.XPATH,
                          '//span[contains(text(),"删除")]/parent::div/following-sibling::div[@class="el-dialog__footer"]//span[contains(text(),"取消")]')
        # 如果是地图模块的删除操作
        elif module_val == "map":
            DELETE_BTN = (By.XPATH,
                           '//span[contains(text(),"删除")]/ancestor::div[@class="el-message-box"]//button//span[contains(text(), "删除")]')
            CANCEL_BTN = (By.XPATH,
                          '//span[contains(text(),"删除")]/ancestor::div[@class="el-message-box"]//button//span[contains(text(), "取消")]')
        elif module_val == "timezone":
            DELETE_BTN = (By.XPATH, '//button//span[contains(text(), "删除")]')
            CANCLE_BTN = (By.XPATH, '//button//span[contains(text(), "取消")]')

        if is_delete:
            # 点击删除按钮
            BasePage(self.driver).click_ele(DELETE_BTN)
        else:
            # 点击取消按钮
            BasePage(self.driver).click_ele(CANCEL_BTN)
