# -*- coding:utf-8 -*-
# @Time: 2020/4/13 15:53
# @Author: wenqin_zhu
# @File: handle_database.py
# @Software: PyCharm


import pymysql


class HandleDB(object):
    """ 封装数据库操作 """

    def __init__(self, host, username, password, database, port=3306):
        """
        初始化数据库信息并创建数据库连接
        :param host: 连接数据库主机 如：10.151.3.96
        :param username: 数据库登录用户名
        :param password: 数据库登录密码
        :param database: 连接的数据库名称 如：senseguard
        :param port: 数据库端口，默认为：3306
        """
        # 默认进行数据库连接，没有设置数据库结果的数据类型
        # self.conn_db = pymysql.connect(host, username, password, database, port, charset='utf8')

        # 推荐：连接数据库的同时并指定数据库结果的返回类型为：字典
        self.conn_db = pymysql.connect(host, username, password, database, port, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        # 建立游标
        self.cursor = self.conn_db.cursor()

    def select_database(self, sql, args=None, is_more=False):
        """
        数据库查询
        :param sql: 查询语句
        :param args: 查询参数。 参数的传参数据格式为：序列类型
        :param is_more: 查询结果是否展示多条。 默认显示一条
        :return: 返回数据库查询结果

        SELECT * / 指定表中的字段名 FROM 表名 [WHERE 条件];
        """
        self.cursor.execute(sql, args=args)
        self.conn_db.commit()
        if is_more:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def update_database(self, sql, args=None):
        """
        数据库更新
        :param sql: 更新语句
        :param args: 参数。包括 字段名对应的值 或 条件参数

        UPDATE 表名 SET 字段名1=值1,[字段名1=值1,……] [WHERE 条件]
        """
        self.cursor.execute(sql, args=args)
        self.conn_db.commit()

    def close(self):
        # 关闭游标
        self.cursor.close()
        # 关闭数据库连接
        self.conn_db.close()


if __name__ == '__main__':

    do_mysql = HandleDB(host="10.151.3.96", username="root", password="UVlY88m9suHLsthK", database="senseguard", port=30446)

    #  调用封装的数据库查询方法
    # 方式-：查询动态传入参数的
    # time_zone = "TimeZone-a1fceba3-1afe-46"
    # sql1 = 'SELECT * FROM senseguard.info_time_zone WHERE time_zone_name=%s;'
    # print(sql1)
    # db_result1 = do_mysql.select_database(sql1, args=(time_zone, ), is_more=False)
    # print(db_result1)
    #
    # # 方式二：查询表内所有
    # sql2 = 'SELECT * FROM senseguard.info_time_zone;'
    # db_result2 = do_mysql.select_database(sql2, is_more=True)
    # print(sql2)
    # print(db_result2)

    # 查询
    data = {"username": "libo"}
    select_sql = 'SELECT pwd_err_num FROM senseguard.info_user where username = %s;'
    result = do_mysql.select_database(sql=select_sql, args=(data["username"],))
    print(result["pwd_err_num"])

    # 修改
    update_sql = 'UPDATE senseguard.info_user SET pwd_err_num=0 WHERE username = %s;'
    do_mysql.update_database(sql=update_sql, args=(data["username"]))

    select_sql = 'SELECT pwd_err_num FROM senseguard.info_user where username = %s;'
    result = do_mysql.select_database(sql=select_sql, args=(data["username"],))
    print(result["pwd_err_num"])
