# -*- coding:utf-8 -*-
# @Time: 2020/3/17 15:31
# @Author: wenqin_zhu
# @File: login_data.py
# @Software: PyCharm


class LoginData:

    # 正向用例数据
    success_login_data = ("zhuwenqin", "888888")

    # 异常测试数据 - 用户名和密码的非空校验
    negative_login_data = [
        {"username": "", "password": "1", "code": "1", "error_info": "用户名不能为空"},
        {"username": "1", "password": "", "code": "1", "error_info": "密码不能为空"}
    ]

    # 异常测试数据 - 密码输入错误次数校验 - 第一次输错测试用例数据
    negative_one_password = [{"username": "libo", "password": "1", "error_info": "用户名或密码有误，请重新输入，您还有 4 次机会"}]

    # 异常测试数据 - 密码输入错误次数校验
    negative_other_data = [
        {"username": "libo", "password": "12", "error_info": "用户名或密码有误，请重新输入，您还有 3 次机会"},
        {"username": "libo", "password": "123", "error_info": "用户名或密码有误，请重新输入，您还有 2 次机会"},
        {"username": "libo", "password": "124", "error_info": "用户名或密码有误，请重新输入，您还有 1 次机会"},
        {"username": "libo", "password": "124", "error_info": "多次输入密码有误,账户已被锁定，请联系IT部门"}
    ]
