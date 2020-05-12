# -*- coding:utf-8 -*-
# @Time: 2020/4/28 14:12
# @Author: wenqin_zhu
# @File: table_list.py
# @Software: PyCharm

import time
from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage
from guard.pages.components.dialog import DialogPage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TableListPage(BasePage):

    def judge_table_list_add_name(self, name):
        """ 判断当前列表内是否存在name元素，如果存在返回True，说明添加成功！反之添加失败，返回False """
        try:
            TABLE_NAME = (By.XPATH, f'//table[@class="el-table__body"]//div[@class="cell" and  text() = "{name}"]')
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(TABLE_NAME))
        except:
            return False
        else:
            return True

    def judge_table_list_delete_name(self, name):
        """ 判断当前列表内是否存在name元素，如果存在返回False，说明删除失败！反之删除成功，返回True """
        try:
            TABLE_NAME = (By.XPATH, f'//table[@class="el-table__body"]//div[@class="cell" and  text() = "{name}"]')
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(TABLE_NAME))
        except:
            return True
        else:
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
        if flag == "view":
            BasePage(self.driver).click_ele(VIEW_ICON)
        elif flag == "edit":
            BasePage(self.driver).click_ele(EDIT_ICON)
        elif flag == "delete":
            BasePage(self.driver).click_ele(DELETE_ICON)
            # 进行弹框删除操作
            DialogPage(self.driver).operation_dialog_btn(btn_text="删除")

    # def table_list_delete(self, is_delete=True):
    #     """  table_list 删除操作 """
    #     if is_delete:
    #         # 点击删除按钮
    #         CONFIRM_BTN = (By.XPATH, '//button//span[text()="删除"]')
    #         ele = BasePage(self.driver).get_ele_locator_by_index(CONFIRM_BTN, 1)
    #         ele.click()
    #     else:
    #         # 点击取消按钮
    #         CONFIRM_BTN = (By.XPATH, '//button//span[text()="取消"]')
    #         ele = BasePage(self.driver).get_ele_locator_by_index(CONFIRM_BTN, 1)
    #         ele.click()

    def table_list_switch(self, name):
        """  table_list 列表状态开关，如任务的启用/禁用 """
        # 定位开关操作
        SWITCH_BTN = (By.XPATH, f'//div[@class="cell" and text()="{name}"]/parent::td/following-sibling::td//div[@class="el-switch"]')
        BasePage(self.driver).click_ele(SWITCH_BTN)
        # 在弹框中确定点击按钮 - 修改状态
        DialogPage(self.driver).operation_dialog_btn()

    # 验证禁用指定任务的启用状态是否成功
    def verify_state_success(self, name):
        """  如果禁用操作结束后，该元素定位表达式存在，则禁用成功 """
        try:
            ELE_EXP = (By.XPATH, f'//div[@class="cell" and text()="{name}"]/parent::td/following-sibling::td//div[@class="el-switch" and not(contains(@class, "is-checked"))]')
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(ELE_EXP))
        except:
            return False
        else:
            return True
