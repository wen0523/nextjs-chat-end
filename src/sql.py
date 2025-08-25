#os
from dotenv import load_dotenv
import os

import sqlite3

# 连接数据库
def connect():
    connection = sqlite3.connect('chat.db')
    connection.row_factory = sqlite3.Row  # 返回字典格式的行
    return connection

# 初始化数据库
def init_db():
    connection = connect()
    cursor = connection.cursor()
    
    # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            theme TEXT
        )
    ''')
    
    # 创建列表表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS allList (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            routerID TEXT UNIQUE
        )
    ''')
    
    # 创建测试表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test (
            id TEXT PRIMARY KEY,
            messages TEXT
        )
    ''')
    
    connection.commit()
    connection.close()

#更新个人信息
def updateUserInfo(theUsername, theTheme):
    try:
        # 数据库连接参数
        connection = connect()

        # 创建游标对象
        cursor = connection.cursor()
        cursor.execute('UPDATE user SET username = ?, theme = ?', (theUsername, theTheme))

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
        cursor = connection.cursor()
        cursor.execute('select username,theme from user;')
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
        cursor = connection.cursor()
        cursor.execute('INSERT or REPLACE into allList (text,routerID) VALUES (?,?)', (text, routerID))

        # 动态创建表(html)
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS "{htmlID}" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ask TEXT NOT NULL,
                answer TEXT NOT NULL)
        ''')

        # 动态创建表(message)
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS "{messageID}" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ask TEXT NOT NULL,
                answer TEXT NOT NULL)
        ''')

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
        cursor = connection.cursor()
        cursor.execute('select * from allList;')
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
        cursor = connection.cursor()
        cursor.execute('delete from allList where routerID = ?', (routerID,))

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
        cursor = connection.cursor()
        cursor.execute(f'INSERT into "{routerID}" (ask, answer) VALUES (?,?)', (askContent, requestContent))

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
        cursor = connection.cursor()
        cursor.execute(f'select * from "{routerID}";')
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
        cursor = connection.cursor()
        cursor.execute(f'INSERT into "{routerID}" (ask, answer) VALUES (?,?)', (askContent, requestContent))

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
        cursor = connection.cursor()
        cursor.execute(f'select * from "{routerID}";')
        result = cursor.fetchall()
        return result

    except Exception as e:
        print(e)
    finally:
        # 关闭数据库连接
        connection.close()