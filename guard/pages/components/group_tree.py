# -*- coding:utf-8 -*-
# @Time: 2020/3/30 19:15
# @Author: wenqin_zhu
# @File: group_tree.py
# @Software: PyCharm

import time
from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage


class GroupTreePage(BasePage):

    # 点击左侧树图分组，通过分组名称
    def click_group_by_name(self, group_name):

        # 定位分组名
        DEPARTMENT_NAME = (By.XPATH, f'//div[@title="{group_name}"]')
        BasePage(self.driver).click_ele(DEPARTMENT_NAME)

    # 点击左侧树图icon，进行创建同级/下一级、详情、重命名和删除操作
    def click_menu_by_name(self, group_name, menu_name):

        # 定位分组右侧icon
        GROUP_ICON = (By.XPATH, f'//div[@title="{group_name}"]/parent::div/following-sibling::div[contains(text(), "︙")]')
        BasePage(self.driver).mouse_move_ele(GROUP_ICON)

        # 通过传入不同的 menu_name 滑动到不同的操作
        GROUP_MENU_NAME = (By.XPATH, f'//div[@id="menu"]//li[@class="menu" and contains(text(), "{menu_name}")]')
        BasePage(self.driver).mouse_move_ele_and_click(GROUP_ICON, GROUP_MENU_NAME)

    def create_dep_group_com(self, group_name, loc_by_til_name, is_confirm=True):
        """
        创建 同级/下一级 分组
        :param group_name: 部门组名称
        :param loc_by_til_name: 通过dialog弹框的标题定位唯一元素
        :param is_confirm: 判断是点击确定还是点击取消按钮 True默认创建点击确定按钮
        """

        # 组名称input框
        GROUP_INPUT = (By.XPATH, f'//span[contains(text(),"{loc_by_til_name}")]/parent::div/following-sibling::div[@class="el-dialog__body"]//input')
        BasePage(self.driver).update_input_text(GROUP_INPUT, group_name)
        if is_confirm:
            # 点击确认按钮
            CONFIRM_BTN = (By.XPATH, f'//span[contains(text(),"{loc_by_til_name}")]/parent::div/following-sibling::div[@class="el-dialog__footer"]//span[contains(text(),"确定")]')
            BasePage(self.driver).click_ele(CONFIRM_BTN)
        else:
            # 点击取消按钮
            CONFIRM_BTN = (By.XPATH, f'//span[contains(text(),"{loc_by_til_name}")]/parent::div/following-sibling::div[@class="el-dialog__footer"]//span[contains(text(),"取消")]')
            BasePage(self.driver).click_ele(CONFIRM_BTN)

    def delete_dep_group_com(self, module_val, is_delete=True):
        # 删除分组
        """
        group_tree分组组件中，弹框删除操作
        :param module_val: 不同模块共用，由于元素定位不一样，需要动态传入删除操作的模块
        :param is_delete:
        :return:
        """
        # 如果是用户模块的删除操作
        if module_val == "user" or module_val == "device":
            # 定位删除按钮
            CONFIRM_BTN = (By.XPATH,
                           '//span[contains(text(),"删除")]/parent::div/following-sibling::div[@class="el-dialog__footer"]//span[contains(text(),"删除")]')
            # 定位取消按钮
            CANCEL_BTN = (By.XPATH,
                           '//span[contains(text(),"删除")]/parent::div/following-sibling::div[@class="el-dialog__footer"]//span[contains(text(),"取消")]')
        # 如果是地图模块的删除操作
        elif module_val == "map":
            CONFIRM_BTN = (By.XPATH, '//span[contains(text(),"删除")]/ancestor::div[@class="el-message-box"]//button//span[contains(text(), "删除")]')
            CANCEL_BTN = (By.XPATH, '//span[contains(text(),"删除")]/ancestor::div[@class="el-message-box"]//button//span[contains(text(), "取消")]')

        if is_delete:
            # 点击删除按钮
            BasePage(self.driver).click_ele(CONFIRM_BTN)
        else:
            # 点击取消按钮
            BasePage(self.driver).click_ele(CANCEL_BTN)

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

    def create_peer_or_next_group(self, group_name=None, parent_name=None, is_peer=True):
        if is_peer:
            # 滑动到创建同级分组
            GroupTreePage(self.driver).click_menu_by_name(parent_name, "创建同级")
            # 动态定位title 为 创建同级
            GroupTreePage(self.driver).create_dep_group_com(group_name, "创建同级")
        else:
            # 滑动到创建下一级分组
            GroupTreePage(self.driver).click_menu_by_name(parent_name, "创建下一级")
            # 动态定位title 为 创建下一级
            GroupTreePage(self.driver).create_dep_group_com(group_name, "创建下一级")

    def delete_peer_or_next_group_by_name(self, group_name=None, parent_name=None, module_val=None, is_peer=True, is_delete=True):
        """
        通过组名称删除分组
        :param group_name: 子级分组
        :param parent_name: 父级分组
        :param module_val: 指定删除操作的模块名 - 由于前端页面元素标签定位不同
        :param is_peer: 判断删除父级/子级分组，默认删除父级
        :param is_delete: 判断点击删除还是取消按钮，默认删除
        """
        if is_peer:
            GroupTreePage(self.driver).click_group_by_name(parent_name)
            # 滑动到删除
            GroupTreePage(self.driver).click_menu_by_name(parent_name, "删除")
        else:
            # 点击父级分组，出现子级分组列表
            GroupTreePage(self.driver).click_group_by_name(parent_name)
            time.sleep(0.5)
            # 滑动到删除
            GroupTreePage(self.driver).click_menu_by_name(group_name, "删除")

        if is_delete:
            # 点击删除按钮
            GroupTreePage(self.driver).delete_dep_group_com(module_val)
        else:
            # 点击取消按钮
            GroupTreePage(self.driver).delete_dep_group_com(module_val, is_delete=False)
