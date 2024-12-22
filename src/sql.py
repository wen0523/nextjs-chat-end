#os
from dotenv import load_dotenv
import os

import pymysql

# 加载 .env 文件
load_dotenv('../.env')

# 获取环境变量
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

#连接数据库
def connect():
    connection = pymysql.connect(
            host=db_host,      # 数据库主机地址
            user=db_user,   # 数据库用户名
            password=db_password,  # 数据库密码
            db='DATACHAT',     # 数据库名称
            charset='utf8mb4',      # 字符编码
            cursorclass=pymysql.cursors.DictCursor  # 返回字典格式的游标
        )
    return connection

#更新个人信息
def updateUserInfo(theUsername, theTheme):
    try:
        # 数据库连接参数
        connection = connect()

        # 创建游标对象
        with connection.cursor() as cursor:
            sql = 'UPDATE user SET username = %s, theme = %s'
            cursor.execute(sql, (theUsername, theTheme))  # 使用参数化查询

            # 提交事务
            connection.commit()
            return 'success'
    except Exception as e:
        connection.rollback()# 在出现错误时回滚事务，防止不完整或错误的数据被写入。
        print(e)
        return 'error'
    finally:
        # 关闭数据库连接
        connection.close()

#获取个人信息
def getUserInfo():
    try:
        # 数据库连接参数
        connection = connect()

        # 创建游标对象
        with connection.cursor() as cursor:
            sql = 'select username,theme from user;'
            # 执行SQL语句
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

    except Exception as e:
        print(e)
    finally:
        # 关闭数据库连接
        connection.close()

#设置列表
def setList(text, routerID, htmlID, messageID):
    try:
        # 数据库连接参数
        connection = connect()

        # 创建游标对象
        with connection.cursor() as cursor:
            sql1 = 'INSERT into allList (text,routerID) VALUES (%s,%s)'
            cursor.execute(sql1, (text, routerID))  # 使用参数化查询

            # 动态创建表(html)
            sql2 = f"""
            CREATE TABLE IF NOT EXISTS `{htmlID}` (
                `ask` TEXT NOT NULL,
                `answer` MEDIUMTEXT NOT NULL);
            """
            cursor.execute(sql2)

            # 动态创建表(message)
            sql3 = f"""
            CREATE TABLE IF NOT EXISTS `{messageID}` (
                `ask` TEXT NOT NULL,
                `answer` MEDIUMTEXT NOT NULL);
            """
            cursor.execute(sql3)

            # 提交事务
            connection.commit()
            return 'success'
    except Exception as e:
        connection.rollback()# 在出现错误时回滚事务，防止不完整或错误的数据被写入。
        print(e)
        return 'error'
    finally:
        # 关闭数据库连接
        connection.close()

#获取列表
def getList():
    try:
        # 数据库连接参数
        connection = connect()

        # 创建游标对象
        with connection.cursor() as cursor:
            sql = 'select * from allList;'
            # 执行SQL语句
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

    except Exception as e:
        print(e)
    finally:
        # 关闭数据库连接
        connection.close()

#删除列表及列表对应的信息
def deleteList(routerID):
    try:
        # 数据库连接参数
        connection = connect()

        # 创建游标对象
        with connection.cursor() as cursor:
            sql = 'delete from allList where routerID = %s'
            cursor.execute(sql, routerID)  # 使用参数化查询 

            # 提交事务
            connection.commit()
            return 'success'
    except Exception as e:
        connection.rollback()# 在出现错误时回滚事务，防止不完整或错误的数据被写入。
        print(e)
        return 'error'
    finally:
        # 关闭数据库连接
        connection.close()

#存储聊天信息（html）
def setHtmlContent(askContent, requestContent, routerID):
    try:
        # 数据库连接参数
        connection = connect()

        # 创建游标对象
        with connection.cursor() as cursor:
            sql = f'INSERT into `{routerID}` VALUES (%s,%s)'
            cursor.execute(sql, (askContent, requestContent))  # 使用参数化查询

            # 提交事务
            connection.commit()
            return 'success'
    except Exception as e:
        connection.rollback()# 在出现错误时回滚事务，防止不完整或错误的数据被写入。
        print(e)
        return 'error'
    finally:
        # 关闭数据库连接
        connection.close()

#获取聊天信息（html）
def getHtmlContent(routerID):
    try:
        # 数据库连接参数
        connection = connect()

        # 创建游标对象
        with connection.cursor() as cursor:
            sql = f'select * from `{routerID}`;'
            # 执行SQL语句
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

    except Exception as e:
        print(e)
    finally:
        # 关闭数据库连接
        connection.close()

#存储聊天信息（message）
def setMessageContent(askContent, requestContent, routerID):
    try:
        # 数据库连接参数
        connection = connect()

        # 创建游标对象
        with connection.cursor() as cursor:
            sql = f'INSERT into `{routerID}` VALUES (%s,%s)'
            cursor.execute(sql, (askContent, requestContent))  # 使用参数化查询

            # 提交事务
            connection.commit()
            return 'success'
    except Exception as e:
        connection.rollback()# 在出现错误时回滚事务，防止不完整或错误的数据被写入。
        print(e)
        return 'error'
    finally:
        # 关闭数据库连接
        connection.close()

#获取聊天信息（message）
def getMessageContent(routerID):
    try:
        # 数据库连接参数
        connection = connect()

        # 创建游标对象
        with connection.cursor() as cursor:
            sql = f'select * from `{routerID}`;'
            # 执行SQL语句
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

    except Exception as e:
        print(e)
    finally:
        # 关闭数据库连接
        connection.close()