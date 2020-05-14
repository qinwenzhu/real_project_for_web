# -*- coding:utf-8 -*-
# @Time: 2020/3/16 11:21
# @Author: wenqin_zhu
# @File: menubar.py
# @Software: PyCharm

from utils.handle_log import HandleLog
from selenium.webdriver.common.by import By
from guard.pages.classes.basepage import BasePage
from selenium.webdriver.support.wait import WebDriverWait
from guard.pages.components.alert_info import AlertInfoPage
from selenium.webdriver.support import expected_conditions as EC


class MenuBarPage(BasePage):

    log = HandleLog().get_logger()

    def click_nav_item(self, menu_text, sub_menu_text=None):
        """
        封装导航栏组件：传入的参数是一级还是二级导航
        :param menu_text: 菜单文本<导航文本的唯一性>
        :param sub_menu_text: 子菜单文本
        :return:
        """

        # 当推送消息过多，系统会弹出消息提示，但是会挡住nav导航条，所以需要在定位元素之前进行判断和关闭
        try:
            INFO_TEXT = (By.XPATH, '//div[@role="alert"]//p')
            # WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(INFO_TEXT))
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(INFO_TEXT))
        except:
            # 此处设置日志的等级为debug，仅仅是为了自己能在控制台中查看，不算抛出异常
            self.log.debug("-------------无消息弹框出现---------------")
        else:
            AlertInfoPage(self.driver).close_alert()

        if menu_text == "工具":
            MENU_TEXT = (By.XPATH, f'//div[text()="{menu_text}"]')
            SUB_MENU_TEXT = (By.XPATH, f'//li[text()="{sub_menu_text}"]')
        else:
            MENU_TEXT = (By.XPATH, f'//em[text()="{menu_text}"]')
            SUB_MENU_TEXT = (By.XPATH, f'//em[text()="{sub_menu_text}"]')

        if sub_menu_text is not None:
            # 通过移动到一级目录然后点击二级目录
            BasePage(self.driver).mouse_move_ele(MENU_TEXT)
            BasePage(self.driver).mouse_move_ele_and_click(MENU_TEXT, SUB_MENU_TEXT)
        else:
            # 选择指定的一级目录
            BasePage(self.driver).click_ele(MENU_TEXT)


if __name__ == '__main__':
    import time
    from selenium import webdriver
    from guard.pages.login_page import LoginPage
    driver = webdriver.Chrome()
    driver.get("http://10.151.3.96/login")
    LoginPage(driver).login("zhuwenqin", "888888", login_way="ssh")
    # 测试点击存在二级导航的
    MenuBarPage(driver).click_nav_item("工具", "人脸属性检测")
    time.sleep(4)
    # 测试点击只存在一级导航
    MenuBarPage(driver).click_nav_item("看板")
    time.sleep(2)
    driver.quit()
