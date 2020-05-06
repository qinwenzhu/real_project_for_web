# -*- coding:utf-8 -*-
# @Time: 2020/3/26 18:52
# @Author: wenqin_zhu
# @File: basepage.py
# @Software: PyCharm

# 导入日期
from datetime import datetime
# 所有浏览器共用的 WebDriver 类
from selenium.webdriver.remote.webdriver import WebDriver
# 导入显性等待
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 鼠标操作 ActionChains
from selenium.webdriver.common.action_chains import ActionChains
# 自定义 - win系统的窗口上传
from guard.tools.custom_upload_file import upload
# 自定义 - 导入日志
from utils.handle_log import HandleLog
# 自定义 - 导入公共路径
from guard.pages.classes.custom_share_path import SharePath


class BasePage:
    """
        BasePage - 针对selenium框架中常用的元素操作进行二次封装
    """

    # 初始化日志对象并返回
    log = HandleLog(r"{}/log.txt".format(SharePath.LOG_FOLDER)).get_logger()

    def __init__(self, driver: WebDriver):
        # 传入 driver - 指定类型为：WebDriver
        self.driver = driver

    def wait_for_ele_to_be_visible(self, loc, timeout=20, poll_frequency=0.5):
        """ 等待元素在页面中可见 """

        self.log.info(f"等待元素可见！---{loc[-1]}---")
        try:
            WebDriverWait(self.driver, timeout, poll_frequency).until(EC.visibility_of_element_located(loc))
        except TimeoutError as e:
            # 对当前页面进行截图
            self.save_web_screenshots()
            self.log.error(f"等待元素可见报错!---{loc[-1]}---")
            raise e

    def wait_for_ele_to_be_presence(self, loc, timeout=10, poll_frequency=0.5):
        """ 等待元素在页面中存在"""

        self.log.info(f"等待元素存在！---{loc[-1]}---")
        try:
            WebDriverWait(self.driver, timeout, poll_frequency).until(EC.presence_of_element_located(loc))
        except TimeoutError as e:
            self.save_web_screenshots()
            self.log.error(f"等待元素存在报错!---{loc[-1]}---")
            raise e

    # def wait_for_ele_to_click(self, loc, img_describe="current", timeout=10, poll_frequency=0.5):
    #     """ 等待元素可点击 """
    #
    #     self.log.info(f"等待元素可点击：{img_describe}页面的-{loc[-1]}元素")
    #     try:
    #         WebDriverWait(self.driver, timeout, poll_frequency).until(EC.element_to_be_clickable(loc))
    #     except TimeoutError as e:
    #         self.save_web_screenshots(img_describe)
    #         self.log.error(f"等待元素可点击失败!")
    #         raise e

    def get_ele_locator(self, loc):
        """ 获取元素 """

        self.log.info(f"获取元素！---{loc[-1]}---")
        try:
            ele = self.driver.find_element(*loc)
        except Exception as e:
            self.save_web_screenshots()
            self.log.error(f"获取元素报错！---{loc[-1]}---")
            raise e
        else:
            return ele

    def get_ele_locator_by_index(self, loc, index):
        """ 页面定位表达式能匹配到多个，通过下标访问 """

        self.log.info(f"获取元素列表！---{loc[-1]}---")
        try:
            ele = self.driver.find_elements(*loc)
        except Exception as e:
            self.save_web_screenshots()
            self.log.error(f"获取元素列表报错！---{loc[-1]}---")
            raise e
        else:
            return ele[index]

    def get_text(self, loc):
        """ 获取元素的文本内容  前提：元素存在 """

        self.wait_for_ele_to_be_presence(loc)
        ele = self.get_ele_locator(loc)
        self.log.info(f"获取元素文本！---{loc[-1]}---")
        try:
            return ele.text
        except Exception as e:
            self.save_web_screenshots()
            self.log.error(f"获取元素文本报错！---{loc[-1]}---")
            raise e

    def get_ele_attribute(self, loc, attr_name):
        """ 获取元素的属性  前提：元素存在 """

        self.wait_for_ele_to_be_presence(loc)
        ele = self.get_ele_locator(loc)
        self.log.info(f"获取元素属性！---{loc[-1]}---")
        try:
            attr_val = ele.get_attribute(attr_name)
        except Exception as e:
            self.save_web_screenshots()
            self.log.error(f"获取元素属性报错！---{loc[-1]}---")
            raise e
        else:
            return attr_val

    def update_input_text(self, loc, val):
        """ 文本框输入文本  前提：元素可见 """

        self.wait_for_ele_to_be_visible(loc)
        ele = self.get_ele_locator(loc)
        self.log.info(f"文本框输入！---{loc[-1]}---")
        try:
            ele.send_keys(val)
        except Exception as e:
            self.save_web_screenshots()
            self.log.error(f"文本框输入报错！---{loc[-1]}---")
            raise e

    def clear_input_default_val(self, loc):
        """ 清空文本框默认值 """

        self.wait_for_ele_to_be_presence(loc)
        ele = self.get_ele_locator(loc)
        self.log.info(f"清空文本框默认值！---{loc[-1]}---")
        try:
            ele.clear()
        except Exception as e:
            self.save_web_screenshots()
            self.log.error(f"清空文本框默认值报错！---{loc[-1]}---")
            raise e

    def upload_file(self, loc, filename=None, upload_way="input", browser_type="chrome"):
        """
        文件上传
        :param loc: 元素定位表达式
        :param filename: 文件上传路径
        :param upload_way: 判断上传文件的类型。input类型或者win文件类型
        :param browser_type: win窗口上传时打开的当前浏览器
        :param img_describe: 截图命名描述
        """

        self.wait_for_ele_to_be_visible(loc)
        ele = self.get_ele_locator(loc)
        try:
            if upload_way == "input":
                self.log.info(f"通过input类型为file的方式进行文件上传！---{loc[-1]}---")
                ele.send_keys(filename)
            elif upload_way == "win":
                self.log.info(f"通过windows窗口的方式进行文件上传！---{loc[-1]}---")
                upload(file_path=filename, browser_type=browser_type)
        except Exception as e:
            self.save_web_screenshots()
            self.log.error(f"文件上传报错！---{loc[-1]}---")
            raise e

    def click_ele(self, loc):
        """ 点击元素，等待元素可见进行点击"""

        self.wait_for_ele_to_be_visible(loc)
        ele = self.get_ele_locator(loc)
        self.log.info(f"点击元素！---{loc[-1]}---")
        try:
            ele.click()
        except Exception as e:
            self.save_web_screenshots()
            self.log.error(f"点击元素报错！---{loc[-1]}---")
            raise e

    """-----------------------------鼠标操作-Actionscharns------------------------------------"""
    def mouse_move_ele(self, loc):
        """  鼠标移动到元素上 """

        actions = ActionChains(self.driver)
        self.wait_for_ele_to_be_visible(loc)
        ele = self.get_ele_locator(loc)
        self.log.info(f"鼠标移动到指定元素！---{loc[-1]}---")
        try:
            actions.move_to_element(ele).perform()
        except Exception as e:
            self.save_web_screenshots()
            self.log.error(f"鼠标移动到指定元素报错！---{loc[-1]}---")
            raise e

    def mouse_move_ele_and_click(self, loc1, loc2, pause_time=2):
        """  鼠标移动到指定元素上并进行列表的点击操作 """

        actions = ActionChains(self.driver)
        # 等待滑动到目标元素可见
        self.wait_for_ele_to_be_visible(loc1)
        move_ele = self.get_ele_locator(loc1)
        # 等待需要操作的元素可见
        self.wait_for_ele_to_be_visible(loc2)
        opera_ele = self.get_ele_locator(loc2)
        self.log.info(f"鼠标移动到A元素---{loc1[-1]}---操作B元素---{loc2[-1]}---！")
        try:
            actions.move_to_element(move_ele).perform()
            actions.pause(pause_time)
            actions.click(opera_ele).perform()
        except Exception as e:
            self.save_web_screenshots()
            self.log.error(f"鼠标移动到A元素---{loc1[-1]}---操作B元素---{loc2[-1]}---报错！")
            raise e

    def mouse_move_to_ele_and_offset(self, x_offset, y_offset, pause_time=2, loc=None, ele=None):
        """  设置鼠标移动到距元素ele，x,y轴指定坐标的距离 """

        actions = ActionChains(self.driver)
        self.log.info(f"鼠标移动到元素---{loc[-1]}---距离x---{x_offset}---,y---{y_offset}---轴的位移！")
        try:
            if loc is not None:
                # 等待滑动到目标元素可见
                self.log.info(f"传入的是元素定位表达！---{loc[-1]}---")
                ele = self.get_ele_locator(loc)
            actions.move_to_element_with_offset(ele, x_offset, y_offset)
            actions.perform()
            actions.pause(pause_time)
            actions.click()
            actions.perform()
        except Exception as e:
            self.save_web_screenshots()
            self.log.error(f"鼠标移动到元素---{loc[-1]}---距离x---{x_offset}---,y---{y_offset}---轴的位移报错！")
            raise e

    def scroll_visibility_region(self, ele=None, loc=None):
        """
        滚动到元素可见区域
        :param ele: 需要滚动到页面可见区域的元素对象
        :param loc: 需要滚动到页面可见的元素定位表达式
        :param img_describe: 当前页面的截图文字介绍
        """
        self.log.info("通过js实现元素滚动到页面可是区域！")
        try:
            if ele is not None:
                self.log.info(f"传参方式为：元素！---{ele}---")
                self.driver.execute_script("arguments[0].scrollIntoView();", ele)
            elif loc is not None:
                self.log.info(f"传传参方式为：元素定位表达！---{loc[-1]}---")
                self.wait_for_ele_to_be_presence(loc)
                element = self.get_ele_locator(loc)
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
        except Exception as e:
            self.save_web_screenshots()
            self.log.error("通过js实现元素滚动到页面可是区域报错！")
            raise e

    def save_web_screenshots(self):
        """ 保存页面截图 """
        current_time_to_str = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
        file_name = f"{current_time_to_str}.jpg"
        self.driver.save_screenshot(f"{SharePath.SCREENSHOT_FOLDER}/{file_name}")
        self.log.info(f"页面截图保存位置：{file_name}")
