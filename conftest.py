# -*- coding:utf-8 -*-
# @Time: 2020/3/25 11:26
# @Author: wenqin_zhu
# @File: conftest.py
# @Software: PyCharm

import time
import uuid
import pytest
import random
from selenium import webdriver
from guard.pages.classes.rtsp import Rtsp
from guard.pages.map_page import MapPage
from guard.pages.tool_page import ToolPage
from guard.pages.task_page import TaskPage
from guard.pages.login_page import LoginPage
from guard.pages.device_page import DevicePage
from guard.pages.components.dialog import DialogPage
from guard.pages.components.menubar import MenuBarPage
from guard.pages.components.alert_info import AlertInfoPage
from guard.pages.components.group_tree import GroupTreePage
from guard.pages.classes.path import SharePath

from utils.handle_config import HandleConfig
from utils.handle_database import HandleDB
# 获取当前的运行的测试环境
from guard.pages.classes.get_run_env import env


""" ---------------------------- 连接数据库 ---------------------------- """
@pytest.fixture(scope="session")
def connect_mysql_and_close():
    # 前置 - 连接数据库 后置 - 关闭连接

    # 读取数据库配置文件中的配置信息
    DB_CONFIG = HandleConfig(r'{}\db_config.yml'.format(SharePath.CONFIG_FOLDER)).config
    db_config = DB_CONFIG.get("database")
    # 通过读取配置文件获取到当前运行环境的ip
    db_config['hostname'] = env()["host"]       # db_config['host'] = "10.151.3.96"
    # 连接数据库
    database = HandleDB(host=db_config['hostname'],
                        username=db_config['user'],
                        password=db_config['password'],
                        port=db_config['port'],
                        database=db_config["database"])
    print("数据库连接成功！")
    yield database
    # 关闭游标、关闭数据库
    database.close()


""" ---------------------------- 启动/关闭 WebDriver服务 ---------------------------- """
@pytest.fixture(scope="module")
def start_driver_and_quit():
    # 前置 - 启动会话窗口 后置 - 关闭
    # driver = webdriver.Chrome()
    # driver.maximize_window()
    # yield driver
    # driver.quit()

    # TODO：优化Jenkins中无法通过 driver.maximize_window() 最大化窗口的问题，
    #  通过chrome浏览器的chrome_options属性进行设置
    # 设置chrome浏览器的options参数
    chrome_options = webdriver.ChromeOptions()
    # 设置浏览器启动的时候就最大化窗口
    chrome_options.add_argument("start-maximized")
    # 启动会话窗口
    driver = webdriver.Chrome(chrome_options=chrome_options)
    yield driver
    driver.quit()


""" ---------------------------- 系统登录 ---------------------------- """
@pytest.fixture(scope="module")
def login(start_driver_and_quit):
    # 成功登录网站
    # 优化：动态传入测试环境  start_driver_and_quit.get("http://10.151.3.96/login")
    start_driver_and_quit.get(f'http://{env()["host"]}/login')
    # 优化：动态传入登陆用户  LoginPage(start_driver_and_quit).login("zhuwenqin", "888888")
    LoginPage(start_driver_and_quit).login(username=f'{env()["username"]}',
                                           password=f'{env()["password"]}',
                                           login_way=env()["login_way"])
    yield start_driver_and_quit


""" ---------------------------- 配置-任务管理 ---------------------------- """
# @pytest.fixture(scope="module")
# 为确保用例数据的高服用低地解耦，此时的scope的级别设置为：class，每个不同的任务都可以调用相同的前置，但相互独立
@pytest.fixture(scope="class")
def task(login, before_structuring_task_common):
    time.sleep(0.5)
    MenuBarPage(login).click_nav_item("配置", "任务管理")
    yield login, before_structuring_task_common


@pytest.fixture(scope="module")
def task_no_setup(login):
    MenuBarPage(login).click_nav_item("配置", "任务管理")
    yield login
    DialogPage(login).close_dialog()


@pytest.fixture
def back_default(login):
    # 批量操作之后返回到默认状态
    yield
    time.sleep(1)
    TaskPage(login).click_back_icon()


@pytest.fixture
def back_car_task_page(login):
    # 批量操作之后返回到车辆违停检测页面的默认状态
    MenuBarPage(login).click_nav_item("记录")
    time.sleep(2)
    yield
    time.sleep(0.5)
    MenuBarPage(login).click_nav_item("配置", "任务管理")
    TaskPage(login).click_left_menu(menu_name="车辆-违停检测任务")


@pytest.fixture
def back_ped_task_page(login):
    # 批量操作之后返回到人体区域入侵页面的默认状态
    MenuBarPage(login).click_nav_item("记录")
    time.sleep(2)
    yield
    time.sleep(0.5)
    MenuBarPage(login).click_nav_item("配置", "任务管理")
    TaskPage(login).click_left_menu(menu_name="人体-区域闯入检测任务")


""" ---------------------------- 配置-设备管理 ---------------------------- """
# @pytest.fixture(scope="module")
@pytest.fixture(scope="class")
def device(login, before_device_common):
    # 进入设备模块
    MenuBarPage(login).click_nav_item("配置", "设备管理")
    yield login, before_device_common


""" ---------------------------- 配置-地图管理 ---------------------------- """
@pytest.fixture(scope="module")
def map_module(login):
    # 进入地图管理模块
    MenuBarPage(login).click_nav_item("配置", "地图管理")
    required_parameters = {"map_group_name": f"FGN-{uuid4_data()}"}
    yield login, required_parameters


""" ---------------------------- 配置-时间条件 ---------------------------- """
@pytest.fixture(scope="module")
def timezone(login):
    # 进入时间条件模块
    MenuBarPage(login).click_nav_item("配置", "时间条件")
    before_name = {"timezone": f"TIME-{get_current_time()}",
                   "holiday_name": f"H-{get_current_time()}",
                   "workday_name": f"W-{get_current_time()}"}
    yield login, before_name


""" ---------------------------- 配置-用户管理 ---------------------------- """
@pytest.fixture(scope="module")
def user(login):
    # 进入用户管理模块
    MenuBarPage(login).click_nav_item("配置", "用户管理")
    sole_name = f"UDN-{uuid4_data()}"
    yield login, sole_name


@pytest.fixture
def del_sub_dep_name_to_default(user, sole_group_name):
    yield
    # 删除Default分组的下一级分组
    GroupTreePage(user[0]).delete_peer_or_next_group_by_name(group_name=sole_group_name, module_val="user", is_peer=False)


@pytest.fixture
def del_dep_name_to_user(user, sole_group_name):
    yield
    # 删除用户自定义分组的同级分组
    if AlertInfoPage(user[0]).get_alert_info() == "创建同级分组成功":
        GroupTreePage(user[0]).delete_peer_or_next_group_by_name(parent_name=sole_group_name, module_val="user")


@pytest.fixture
def del_sub_dep_name_to_user(user, sole_group_name):
    yield
    # 删除用户自定义分组的下一级分组
    if AlertInfoPage(user[0]).get_alert_info() == "创建下一级分组成功":
        GroupTreePage(user[0]).delete_peer_or_next_group_by_name(group_name=sole_group_name, parent_name=user[1], module_val="user", is_peer=False)


""" ---------------------------- 工具模块 ---------------------------- """
@pytest.fixture()
def close_tool(login):
    # 后置：关闭当前处于打开状态的小工具窗口
    yield
    ToolPage(login).close_tool()

# @pytest.fixture(scope="function")
# def tool_close_one_to_one_face_compare(login):
#     # 后置：关闭当前窗口 - 1:1人脸验证
#     yield
#     ToolPage(login).close_tool_current_win("tools-face-verification")

# @pytest.fixture
# def tool_close_one_img_quality(login):
#     # 后置：关闭当前窗口 - 质量分数检测
#     yield
#     ToolPage(login).close_tool_current_win("tools-score-detection")
#
# @pytest.fixture
# def tool_close_face_score_detection(login):
#     # 后置：关闭当前窗口 - 人脸属性检测
#     yield
#     ToolPage(login).close_tool_current_win("tools-test-detection")


""" ---------------------------- 登录模块 ---------------------------- """
@pytest.fixture
def setup_login():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(f'http://{env()["host"]}/login')          # start_driver_and_quit.get("http://10.151.3.96/login")
    yield driver
    driver.quit()


""" ---------------------------- 共用 ---------------------------- """
@pytest.fixture
def close_alert_info(login):
    # 关闭alert消息弹框
    yield
    AlertInfoPage(login).close_alert()


@pytest.fixture
def close_dialog(login):
    # 关闭dialog
    yield
    DialogPage(login).close_dialog()


""" ---------------------------- 通用的唯一标识码 ---------------------------- """
@pytest.fixture()
def uuid4_para():
    uid = str(uuid.uuid4())
    suid = ''.join(uid.split('-'))
    yield suid


@pytest.fixture
def sole_group_name():
    sole_name = f"UNIQUE-{get_current_time()}"
    yield sole_name


@pytest.fixture
def overlong_name():
    sole_name = f"ABD-{uuid4_data()}"
    yield sole_name


""" ---------------------------- 共用前置条件 ---------------------------- """
# @pytest.fixture(scope="module")
@pytest.fixture(scope="class")
def before_device_common(login):

    # before_name = {"floor_group_name": f"FGN-{get_current_time()}"}
    # 将相关联的前置数据，写在同一个地方
    before_name = {"floor_group_name": f"FGN-{get_current_time()}",
                   "device_group_name": f"DGN-{get_current_time()}",
                   "device_name": f"DN-{get_current_time()}",
                   "task_name": f"TN-{get_current_time()}"}

    # 进入地图模块，创建地图分组，上传地图
    time.sleep(0.5)
    MenuBarPage(login).click_nav_item("配置", "地图管理")
    time.sleep(1)
    GroupTreePage(login).create_peer_or_next_group(group_name=before_name["floor_group_name"])
    MapPage(login).upload_map(file_name=r"{}/map_data/company_4th_floor.jpg".format(SharePath.DATA_FOLDER),
                              group_name=before_name["floor_group_name"])
    yield before_name
    # 删除地图分组
    time.sleep(0.5)
    MenuBarPage(login).click_nav_item("配置", "地图管理")
    time.sleep(0.2)
    GroupTreePage(login).delete_peer_or_next_group_by_name(module_val="map", parent_name=before_name["floor_group_name"])


# @pytest.fixture(scope="module")
@pytest.fixture(scope="class")
def before_structuring_task_common(login, before_device_common):
    # 进入设备模块，创建设备分组和对应对应类型的设备
    time.sleep(0.5)
    MenuBarPage(login).click_nav_item("配置", "设备管理")
    before_name = uuid4_data()
    rtsp_para = Rtsp(device_name=before_device_common["device_name"], device_id=before_name, group_name=before_device_common["device_group_name"],
                floor_name=before_device_common["floor_group_name"], rtsp_address="rtsp://10.151.3.119:7554/IMG_0322.264")
    # 创建设备 - 网络摄像机 - RTSP
    time.sleep(1)
    GroupTreePage(login).create_peer_or_next_group(group_name=before_device_common["device_group_name"])
    time.sleep(2)
    DevicePage(login).add_device_by_type(rtsp_para, device_type="网络摄像机")
    yield before_device_common
    MenuBarPage(login).click_nav_item("配置", "设备管理")
    # 删除相对于Default分组的同级设备分组
    GroupTreePage(login).delete_peer_or_next_group_by_name(module_val="device", parent_name=before_device_common["device_group_name"])


""" ---------------------------- 自定义方法 ---------------------------- """


def get_current_time():
    # 获取当前系统时间时间
    return time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))


def uuid4_data():
    # 生成随机数据
    return str(uuid.uuid4())


def integer_num():
    # 生成指定范围内的整数
    return random.randint(1, 60)
