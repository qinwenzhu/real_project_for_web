# -*- coding:utf-8 -*-
# @Time: 2020/3/17 10:05
# @Author: wenqin_zhu
# @File: test_login.py
# @Software: PyCharm


import pytest
from guard.pages.login_page import LoginPage
from guard.datas.login_data import LoginData
from guard.pages.components.alert_info import AlertInfoPage


@pytest.mark.smoke
@pytest.mark.positive
def test_login_success(setup_login):
    # 登录成功校验
    LoginPage(setup_login).login(*LoginData.success_login_data)
    # 断言 - 只要返回True，则Pass
    assert LoginPage(setup_login).is_login_success()


@pytest.mark.negative
class TestLoginNegative:
    """ 反向测试类 """
    @pytest.mark.parametrize("data", LoginData.negative_login_data)
    def test_login_fail(self, setup_login, data):
        # 用户名和密码的非空校验
        LoginPage(setup_login).login(data["username"], data["password"], code=data["code"])
        result = LoginPage(setup_login).get_login_error_info()
        assert data["error_info"] in result

    def test_code_error(self, setup_login):
        # 测试验证码错误 - 前端提示信息
        LoginPage(setup_login).login(*LoginData.success_login_data, code="123456")
        result = AlertInfoPage(setup_login).get_alert_info()
        assert "验证码错误" in result

    """    
    测试用户登录密码输错次数到锁定账户校验
    操作步骤：
    查询测试数据中的登录用户在数据库中的字段[密码错误次数]，是否为0
        如果为0，开始执行验证密码输错次数的用例
        否则
        1、修改数据库语句，设置测试数据中的登录用户名的{密码错误次数为0}
        2、开始执行验证密码输错次数的用例
    """
    @pytest.mark.parametrize("data", LoginData.negative_one_password)
    def test_one_error_password(self, connect_mysql_and_close, setup_login, data):
        # 测试第一次密码输入错误的用例
        select_sql = 'SELECT pwd_err_num FROM senseguard.info_user where username = %s;'
        result = connect_mysql_and_close.select_database(sql=select_sql, args=(data["username"],))
        # print(result)
        if result["pwd_err_num"] == 0:
            LoginPage(setup_login).login(data["username"], data["password"])
        else:
            update_sql = 'UPDATE senseguard.info_user SET pwd_err_num=0 WHERE username = %s;'
            connect_mysql_and_close.update_database(sql=update_sql, args=(data["username"]))
            LoginPage(setup_login).login(data["username"], data["password"])
        result = AlertInfoPage(setup_login).get_alert_info()
        assert data["error_info"] in result

    @pytest.mark.parametrize("data", LoginData.negative_other_data)
    def test_other_error_password(self, connect_mysql_and_close, setup_login, data):
        # 测试后面几次密码输错的测试用例，直至账户被锁定
        LoginPage(setup_login).login(data["username"], data["password"])
        result = AlertInfoPage(setup_login).get_alert_info()
        assert data["error_info"] in result
