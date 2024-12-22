id = ''
message = ''

def setID(new_id, new_message):
    global id
    global message
    id = new_id
    message = new_message

def getID():
    all = {
        'id': id,
        'message': message
    }
    return all