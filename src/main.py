#langchain
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

#flask
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sse import sse

import json

#自定义函数
from chat import Chat
from shared_parameters import setID
from sql import updateUserInfo, getUserInfo, setList, getList,deleteList,setHtmlContent,getHtmlContent
from memory import getMemory

##没有进行前端传输过来的数据合法性检测

app = Flask(__name__)
# 正确设置 Redis URL
app.config["REDIS_URL"] = "redis://localhost:6379/0"  # 默认的 Redis 地址和端口
app.register_blueprint(sse, url_prefix='/stream')

# 配置 CORS，允许指定来源访问
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})

chatApp = Chat()
allIDs = [] #用于储存正在使用的routerID，用于消息持久性

@app.route('/chat', methods=['POST'])
def main():
    input = request.form.get('content')
    id= request.form.get('id')
    # language = "zh"
    config = {"configurable": {"thread_id": id}}

    input_messages = ''

    if id in allIDs:
        #如果存在说明可以已经记住历史消息
        input_messages = [HumanMessage(input)]
    else:
        #如果不存在说明没有记住历史消息，获取历史消息并储存
        input_messages = getMemory(id)
        input_messages.append(HumanMessage(input))
        allIDs.append(id)

    for chunk, metadata in chatApp.stream(
        {"messages": input_messages},
        config,
        stream_mode="messages",
    ):  
        try:
            setID(id,input)
            if isinstance(chunk, AIMessage):  # Filter to just model responses
                # 封装为 JSON 格式
                json_message = json.dumps({"content": chunk.content})
                sse.publish(json_message, type='message')
        except EOFError as e:
            print(e)

    return 'success'

#更新个人信息
@app.route('/setBaInfor', methods=['POST'])
def setBaInfor():
    theTheme = request.form.get('theme')
    theUsername = request.form.get('username')

    result = updateUserInfo(theUsername,theTheme)

    return jsonify(result)

#获得个人信息
@app.route('/getBaInfor', methods=['POST'])
def getBaInfor():
    info = getUserInfo()

    return jsonify(info)

#设置全部列表
@app.route('/setallList', methods=['POST'])
def setallList():
    text = request.form.get('text')
    routerID = request.form.get('routerID')
    htmlID = 'html'+routerID
    messageID = 'message'+routerID
    allIDs.append(routerID)

    result = setList(text,routerID,htmlID,messageID)

    return jsonify(result)

#获得全部列表信息
@app.route('/getallList', methods=['POST'])
def getallList():
    allList = getList()

    return jsonify(allList)

#删除列表
@app.route('/delallList', methods=['POST'])
def delallList():
    routerID = request.form.get('routerID')
    
    result = deleteList(routerID)

    return jsonify(result)

#存储聊天信息（html）
@app.route('/setContent', methods=['POST'])
def setContent():
    askContent = request.form.get('ask')
    requestContent = request.form.get('request')
    routerID = 'html'+request.form.get('routerID')
    
    result = setHtmlContent(askContent,requestContent,routerID)

    return jsonify(result)

#获取聊天信息（html）
@app.route('/getContent', methods=['POST'])
def getContent():
    routerID = 'html'+request.form.get('routerID')

    htmlContent = getHtmlContent(routerID) 

    return jsonify(htmlContent)
    
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)