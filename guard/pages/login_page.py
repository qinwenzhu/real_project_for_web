# -*- coding:utf-8 -*-
# @Time: 2020/3/17 10:17
# @Author: wenqin_zhu
# @File: login_page.py
# @Software: PyCharm

# 导入正则表达式
import re
import time

# 导入元素的定位方式
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 导入第三方验证码识别接口
from guard.tools.chaojiying import Chaojiying_Client
import urllib.request

# 导入封装类
from guard.tools.redis_database import GetRedisData
from utils.ssh import SSH
from utils.handle_config import HandleConfig

# 导入共用路径
from guard.pages.classes.custom_share_path import SharePath

# 导入二次封装selenium框架的 BasePage类
from guard.pages.classes.basepage import BasePage
from guard.pages.classes.get_run_env import env


class LoginPage(BasePage):

    def login(self, username, password, code=None, login_way="default"):
        """ 登录 """

        # 登录用户名文本框
        USERNAME_INPUT = (By.CSS_SELECTOR, 'input[name="username"]')
        # 登录密码文本框
        PASSWORD_INPUT = (By.CSS_SELECTOR, 'input[name="password"]')
        # 登录验证码文本框
        CODE_INPUT = (By.CSS_SELECTOR, 'input[name="verifyCode"]')
        # 定位到登录按钮
        LOGIN_BUTTON = (By.XPATH, '//button//span[contains(text(), "登录")]')

        # 输入用户名 - 等待元素可见并输入文本
        BasePage(self.driver).update_input_text(USERNAME_INPUT, username)
        # 输入密码
        BasePage(self.driver).update_input_text(PASSWORD_INPUT, password)

        if code is None:
            """ 获取登录验证码的不同方式 """
            if login_way == "default":
                # 1、通过redis的方式获取登录验证码
                code = self.get_captcha_from_redis()
            elif login_way == "cjy":
                # 2、通过调用第三方接口<cjy>识别登录验证码
                code = self.get_code_cjy()
            elif login_way == "ssh":
                # 定位到刷新验证码按钮，并在读取验证码之前先点击刷新
                CAPTCHA_REFRESH_BUTTON = (By.CSS_SELECTOR, 'div.verify-code > div.refresh > i')
                BasePage(self.driver).click_ele(CAPTCHA_REFRESH_BUTTON)
                time.sleep(0.2)
                # 3、通过ssh连接到服务器，从日志里获取登录验证码
                code = self.get_captcha_from_k8s_log()
            elif login_way == 'ocr':
                # 4、通过ocr智能识别获取登录验证码
                # code = get_code_by_ocr()
                pass
            elif login_way == 'debug':
                # 调试的时候，通过手动从控制台输入的方式获取登录验证码
                print("请手动输入登录页面的验证码：")
                code = input()
        # 输入得到的验证码
        BasePage(self.driver).update_input_text(CODE_INPUT, code)

        # 点击登录网站
        BasePage(self.driver).click_ele(LOGIN_BUTTON, "登录")

    def is_login_success(self):
        # 判断是否登录成功：如果能定位到 USERNAME 元素，登录成功<返回True>，否则返回 False
        try:
            USERNAME = (By.CSS_SELECTOR, 'span[class="avatar-name"]')
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(USERNAME))
        except:
            print("-------------等待用户名元素存在失败！---------------")
            return False
        else:
            return True

    def get_login_error_info(self):
        # 获取到登陆页面的错误提示信息

        ERROR_INFO = (By.XPATH, '//div[@class="el-form-item__error"]')
        return BasePage(self.driver).get_text(ERROR_INFO)

    def get_code_cjy(self):
        """ 通过调用第三方接口获取验证码"""
        CODE_IMG = (By.CSS_SELECTOR, '.code-pic > img')
        BasePage(self.driver).wait_for_ele_to_be_visible(CODE_IMG, "登录")
        code_img_src = BasePage(self.driver).get_ele_locator(CODE_IMG).get_attribute("src")
        # 将获取到的图片地址保存到本地目录
        urllib.request.urlretrieve(code_img_src, r'{}\cjy\login_code.jpg'.format(SharePath.DATA_FOLDER))
        # 调第三方接口_识别验证码
        cjy = Chaojiying_Client('18500379756', '123456', '9bf661c27903e244883b5af71ed0c5da')            # 用户中心>>软件ID 生成一个
        img = open(r'{}\cjy\login_code.jpg'.format(SharePath.DATA_FOLDER), 'rb').read()    # 本地图片文件路径,有时WIN系统须要//
        result = cjy.PostPic(img, 1902)  # 1902 验证码类型
        print(f"-------第三方接口识别当前的验证码为：{result['pic_str']}-----------")
        return result['pic_str']

    def get_captcha_from_k8s_log(self):
        SSH_CONFIG = HandleConfig(r'{}\ssh_config.yml'.format(SharePath.CONFIG_FOLDER)).config
        ssh_config = SSH_CONFIG.get("ssh")
        # 动态传入当前运行环境的ip
        ssh_config['hostname'] = f'{env()["host"]}'                             # ssh_config['hostname'] = "10.151.3.96"
        ssh = SSH(**ssh_config)
        oauth2_pod_name = ssh.execute_command(
            "kubectl get pods | grep oauth2 | awk '{print $1}'")
        captcha = ssh.execute_command(
            f"kubectl logs {oauth2_pod_name.rstrip()} --tail 2 | grep 生成验证码存入redis | awk -F ' ' '{{print $5}}'")
        return captcha.rstrip()

    def get_captcha_from_redis(self):
        """ 通过Redis获取验证码 """
        img_url = self.driver.find_element_by_xpath("//*[@class='code-pic']/img").get_attribute("src")
        # print(img_url)
        # 获取到 img_url = 'http://10.151.3.96/senseguard-oauth2/api/v1/kaptcha?timestamp=4173971161777936'

        timestamp = re.findall(".*timestamp=(\d+)", img_url)
        # print(timestamp)  # 获取到 timestamp = ['4173971161777936']

        # 动态传入环境 ip
        redis = GetRedisData(ip=env()["host"])          # redis = GetRedisData(ip="10.151.3.96")

        # 此处传入的key值可以在连接Redis成功之后通过 .keys获取当前连接池中所有的key进行筛选到执行的Redis的key值
        captcha_code = redis.get_result_from_redis(f"Senseguard:Oauth2:Login:{timestamp[0]}")
        # print(f"当前获取到的验证码为：{captcha_code}")
        return captcha_code


if __name__ == '__main__':
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.get("http://10.151.3.96/login")
    # 测试ssh连接服务器进行验证码获取来进行登录
    # LoginPage(driver).login("zhuwenqin", "888888", login_way="ssh")
    # 设置默认通过redis来识别验证码并进行登录
    LoginPage(driver).login("zhuwenqin", "888888")
    time.sleep(4)
    driver.quit()
