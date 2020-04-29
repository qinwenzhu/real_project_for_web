# -*- coding:utf-8 -*-
# @Time: 2020/4/28 14:12
# @Author: wenqin_zhu
# @File: table_list.py
# @Software: PyCharm

import time
from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage
from guard.pages.classes.web_global_dialog import GlobalDialog


class TableListPage(BasePage):

    def judge_table_list_add_name(self, name):
        """ 判断列表内是否存在当前名称的列表， 存在返回 True """
        TABLE_NAME = (By.XPATH, f'//table[@class="el-table__body"]//div[@class="cell" and  text() = "{name}"]')
        try:
            if self.driver.find_element(*TABLE_NAME):
                return True
        except:
            return False

    def judge_table_list_delete_name(self, name):
        """ 判断列表内是否存在当前名称的列表  不存在返回 True"""
        TABLE_NAME = (By.XPATH, f'//table[@class="el-table__body"]//div[@class="cell" and  text() = "{name}"]')
        try:
            if not self.driver.find_element(*TABLE_NAME):
                return True
        except:
            return False

    def operations_table_list(self, name, flag):
        """ 定位列表项的相关操作，有：查看、编辑、删除 """
        # 定位查看icon
        VIEW_ICON = (By.XPATH, f'//table[@class="el-table__body"]//div[@class="cell" and  text() = "{name}"]/parent::td/following-sibling::td[contains(@class, "tables-operate")]//i[contains(@class, "icon-view")]')
        # 定位编辑icon
        EDIT_ICON = (By.XPATH, f'//table[@class="el-table__body"]//div[@class="cell" and  text() = "{name}"]/parent::td/following-sibling::td[contains(@class, "tables-operate")]//i[contains(@class, "icon-edit")]')
        # 定位删除icon
        DELETE_ICON = (By.XPATH, f'//table[@class="el-table__body"]//div[@class="cell" and  text() = "{name}"]/parent::td/following-sibling::td[contains(@class, "tables-operate")]//i[contains(@class, "icon-delete")]')

        # 点击查看、 编辑、删除icon
        time.sleep(2)
        if flag == "view":
            BasePage(self.driver).click_ele(VIEW_ICON)

            # TODO 弹框操作
            pass

        elif flag == "edit":
            BasePage(self.driver).click_ele(EDIT_ICON)

            # TODO 弹框操作
            pass

        elif flag == "delete":
            time.sleep(2)
            BasePage(self.driver).click_ele(DELETE_ICON)
            # 进行弹框删除操作
            self.table_list_delete()

    def table_list_delete(self, is_delete=True):
        """  table_list 删除操作 """
        if is_delete:
            # 点击删除按钮
            CONFIRM_BTN = (By.XPATH, '//button//span[text()="删除"]')
            ele = BasePage(self.driver).get_ele_locator_by_index(CONFIRM_BTN, 1)
            ele.click()
        else:
            # 点击取消按钮
            CONFIRM_BTN = (By.XPATH, '//button//span[text()="取消"]')
            ele = BasePage(self.driver).get_ele_locator_by_index(CONFIRM_BTN, 1)
            ele.click()

    def table_list_switch(self, name):
        """  table_list 列表状态开关，如任务的启用/禁用 """

        # 定位开关操作
        SWITCH_BTN = (By.XPATH, f'//div[@class="cell" and text()="{name}"]/parent::td/following-sibling::td//div[@class="el-switch"]')
        BasePage(self.driver).click_ele(SWITCH_BTN)

        # 在弹框中点击修改状态
        GlobalDialog(self.driver).dialog_delete()
