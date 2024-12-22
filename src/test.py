import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import pymysql
# 加载 .env 文件
load_dotenv('../.env')

# 获取环境变量
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
api_key = os.getenv('API_KEY')

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

connection = connect()

allMessages = {}

def getAllID():
    try:
        # 数据库连接参数
        connection = connect()

        # 创建游标对象
        with connection.cursor() as cursor:
            sql = 'SELECT id FROM test'
            cursor.execute(sql)  # 使用参数化查询
            result = cursor.fetchall()
            id = []
            for row in result:
                id.append(row['id'])
            return id
    except Exception as e:
        connection.rollback()# 在出现错误时回滚事务，防止不完整或错误的数据被写入。
        print(e)
        return 'error'
    finally:
        # 关闭数据库连接
        connection.close()

ids = getAllID()

def getData(routerID, text):
    try:
        # 数据库连接参数
        connection = connect()

        # 创建游标对象
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM test WHERE id = %s'
            cursor.execute(sql, (routerID,))  # 使用参数化查询
            result = cursor.fetchall()
            return result
    except Exception as e:
        connection.rollback()# 在出现错误时回滚事务，防止不完整或错误的数据被写入。
        print(e)
        return 'error'
    finally:
        # 关闭数据库连接
        connection.close()

def updateData(routerID, text):
    try:
        # 数据库连接参数
        connection = connect()

        # 创建游标对象
        with connection.cursor() as cursor:
            if routerID in ids:  
                sql = 'UPDATE test SET messages = %s WHERE id = %s'
                cursor.execute(sql, (text, routerID))  # 使用参数化查询
            else:
                sql = 'INSERT INTO test (id, messages) VALUES (%s, %s)'
                cursor.execute(sql, ('12', 'text'))

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

model = ChatOpenAI(
    model="gpt-3.5-turbo",
    openai_api_base='https://xiaoai.plus/v1',
    openai_api_key= api_key
)


# Define a new graph
workflow = StateGraph(state_schema=MessagesState)


# Define the function that calls the model
def call_model(state: MessagesState):
    response = model.invoke(state["messages"])
    return {"messages": response}#专门用来保存消息的state


# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = MemorySaver()
workflow.compile(checkpointer=memory)

from chat import Chat
from shared_parameters import setID
app = Chat()


################################
language = "English"

query = "Hi! I'm Bob."

input_messages = [HumanMessage(query)]
for chunk, metadata in app.stream(
    {"messages": input_messages, "language": language},
    config,
    stream_mode="messages",
):
    setID(id)
    if isinstance(chunk, AIMessage):  # Filter to just model responses
        print(chunk.content, end="")

query = "What's my name?"
id='456'
config = {"configurable": {"thread_id": id}}
input_messages = [HumanMessage(query)]
for chunk, metadata in app.stream(
    {"messages": input_messages, "language": language},
    config,
    stream_mode="messages",
):
    setID(id)
    if isinstance(chunk, AIMessage):  # Filter to just model responses
        print(chunk.content, end="")

##############################################

# config = {"configurable": {"thread_id": "abc789"}}
# query = "请写一篇关于春的作文，字数要求不少于500字。"
# language = "zh"

# input_messages = [HumanMessage(query)]
# for chunk, metadata in app.stream(
#     {"messages": input_messages, "language": language},
#     config,
#     stream_mode="messages",
# ):
#     if isinstance(chunk, AIMessage):  # Filter to just model responses
#         print(chunk.content, end="|")