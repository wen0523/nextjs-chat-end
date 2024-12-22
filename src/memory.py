from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from sql import getMessageContent

def getMemory(id):
    messages = getMessageContent('message'+id)
    memory = []

    if len(messages) != 0:
        #先判断第一个是不是system,answer储存'system'作为标志
        if messages[0]['answer'] == 'system':
            memory.append(SystemMessage(messages[0]['ask']))
        else:
            memory.append(HumanMessage(messages[0]['ask']))
            memory.append(AIMessage(messages[0]['answer']))
    
        for i in range(1,len(messages)):
            memory.append(HumanMessage(messages[i]['ask']))
            memory.append(AIMessage(messages[i]['answer']))

    return memory
