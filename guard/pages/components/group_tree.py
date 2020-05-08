# -*- coding:utf-8 -*-
# @Time: 2020/3/30 19:15
# @Author: wenqin_zhu
# @File: group_tree.py
# @Software: PyCharm

import time
from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage
from guard.pages.components.dialog import DialogPage


class GroupTreePage(BasePage):

    # 点击左侧树图分组，通过分组名称
    def click_group_by_name(self, group_name="Default"):
        """
        点击树图分组
        :param group_name: 分组名称
        """

        # 定位分组名
        DEPARTMENT_NAME = (By.XPATH, f'//div[@title="{group_name}"]')
        BasePage(self.driver).click_ele(DEPARTMENT_NAME)

    # 创建同级/下一级分组
    def create_peer_or_next_group(self, group_name=None, parent_name="Default", is_peer=True, is_confirm=True):
        """
        创建同级/下一级分组
        :param group_name: 当前需要创建的分组名
        :param parent_name: 通过哪个父级分组来创建，默认通过Default分组创建
        :param is_peer: 创建同级/下一级，默认同级
        """

        if is_peer:
            """ 如果创建同级，先点击分组名，然后滑动该分组进行menu菜单的选择和点击"""
            GroupTreePage(self.driver).click_group_by_name(parent_name)
            GroupTreePage(self.driver).click_menu_name_by_move_icon(parent_name, menu_name="创建同级")
            if is_confirm:
                # 通过dialog对话框 - 创建同级
                DialogPage(self.driver).create_group_by_dialog_title_name(loc_by_til="创建同级", group_name=group_name)
            else:
                DialogPage(self.driver).create_group_by_dialog_title_name(loc_by_til="创建同级", group_name=group_name, is_confirm=False)
        else:
            """ 否则创建下一级，先点击父级分组名，然后滑动该分组进行menu菜单的选择和点击"""
            GroupTreePage(self.driver).click_group_by_name(parent_name)
            # 滑动到icon并选择创建下一级分组
            GroupTreePage(self.driver).click_menu_name_by_move_icon(parent_name, menu_name="创建下一级")
            if is_confirm:
                # 通过dialog对话框 - 创建下一级
                DialogPage(self.driver).create_group_by_dialog_title_name(loc_by_til="创建下一级", group_name=group_name)
            else:
                DialogPage(self.driver).create_group_by_dialog_title_name(loc_by_til="创建下一级", group_name=group_name, is_confirm=False)

    # 删除同级/下一级分组
    def delete_peer_or_next_group_by_name(self, module_val, group_name=None, parent_name="Default", is_peer=True, is_delete=True):
        """
        通过组名称删除分组
        :param module_val: 指定删除操作的模块名 - 由于前端页面元素标签定位不同
        :param group_name: 子级分组
        :param parent_name: 父级分组
        :param is_peer: 判断删除父级/子级分组，默认删除父级
        :param is_delete: 判断点击删除还是取消按钮，默认删除
        """
        if is_peer:
            # 点击分组名
            GroupTreePage(self.driver).click_group_by_name(parent_name)

            # 滑动到icon并点击删除
            GroupTreePage(self.driver).click_menu_name_by_move_icon(parent_name, "删除")
        else:

            # 点击父级分组，出现子级分组列表
            GroupTreePage(self.driver).click_group_by_name(group_name=parent_name)
            # 点击子级分组
            GroupTreePage(self.driver).click_group_by_name(group_name=group_name)

            # 滑动到icon并点击删除
            GroupTreePage(self.driver).click_menu_name_by_move_icon(group_name, "删除")

        if is_delete:
            # 点击删除按钮
            DialogPage(self.driver).is_delete_or_cancel(module_val)
        else:
            # 点击取消按钮
            DialogPage(self.driver).is_delete_or_cancel(module_val, is_delete=False)

    # 滑动到左侧树图icon，选择[创建同级/下一级、详情、重命名和删除]menu选项
    def click_menu_name_by_move_icon(self, group_name, menu_name):
        """
        滑动到icon进行menu菜单选择操作
        :param group_name: 组名称
        :param menu_name: 组右侧动态出现的菜单选择操作
        """

        # 定位分组右侧icon
        GROUP_ICON = (By.XPATH, f'//div[@title="{group_name}"]/parent::div/following-sibling::div[contains(text(), "︙")]')
        # 定位menu容器
        MENU = (By.ID, 'menu')
        # 通过传入不同的 menu_name 滑动到不同的操作
        MENU_NAME = (By.XPATH, f'//div[@id="menu"]//li[@class="menu" and contains(text(), "{menu_name}")]')

        time.sleep(1)
        # 滑动到icon元素上
        BasePage(self.driver).mouse_move_ele(GROUP_ICON)
        # 滑动到menu元素上并点击操作名，如：创建同级
        BasePage(self.driver).mouse_move_ele_and_click(MENU, MENU_NAME)

    def search_dep_by_name(self, group_name):

        # 定位搜索文本框
        SEARCH_INPUT = (By.XPATH, '//aside[@class="el-aside"]//div[contains(@class,"el-input--suffix")]/input')
        BasePage(self.driver).update_input_text(SEARCH_INPUT, group_name)

        # 点击搜索
        SEARCH_BTN = (By.XPATH, '//aside[@class="el-aside"]//div[contains(@class,"el-input--suffix")]/span')
        BasePage(self.driver).click_ele(SEARCH_BTN)

    def judge_search_success(self, group_name):
        # 判断 tree分组下搜索到对应的分组
        RESULT_TEXT = (By.XPATH, f'//div[@role="tree"]//div[contains(@title,"{group_name}")]')
        return BasePage(self.driver).get_text(RESULT_TEXT)

