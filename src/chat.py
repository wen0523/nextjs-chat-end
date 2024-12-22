#os
from dotenv import load_dotenv
import os

#langchain
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

#自定义函数
from shared_parameters import getID
from sql import setMessageContent

# 加载 .env 文件
load_dotenv('../.env')

api_key = os.getenv('API_KEY')

def Chat():
    #连接大模型
    model = ChatOpenAI(
        model="gpt-3.5-turbo",
        openai_api_base='https://xiaoai.plus/v1',
        openai_api_key= api_key
    )

    ##消息持久化
    # 定义一个新的图
    workflow = StateGraph(state_schema=MessagesState)

    # 定义调用模型的函数
    def call_model(state: MessagesState):
        response = model.invoke(state["messages"])
        allData = getID()
        setMessageContent(allData['message'], response.content, 'message'+allData['id'])
        
        return {"messages": response}

    # 定义图中的（单一）节点
    workflow.add_edge(START, "model")
    workflow.add_node("model", call_model)

    # 添加内存
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)

    return app