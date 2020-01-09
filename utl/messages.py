from .models import db, Message

def getMessages(userID, contactID):
<<<<<<< HEAD
    sentMessages = Message.query.filter_by(senderID=userID, receiverID=contactID).order_by(Message.timestamp.asc()).all()
    receivedMessages = Message.query.filter_by(senderID=contactID, receiverID=userID).order_by(Message.timestamp.asc()).all()
    messages = []
    messages.append(sentMessages)
    messages.append(receivedMessages)
=======
    # sentMessages = Message.query.filter_by(senderID=userID, receiverID=contactID).order_by(Message.timestamp.asc()).all()
    # receivedMessages = Message.query.filter_by(senderID=contactID, receiverID=userID).order_by(Message.timestamp.asc()).all()
    # messages = []
    # messages.append(sentMessages)
    # messages.append(receivedMessages)
    # return messages
    messages = Message.query.filter(((Message.senderID==userID) & (Message.receiverID==contactID)) | ((Message.senderID==contactID) & (Message.receiverID==userID))).order_by(Message.timestamp.asc())
>>>>>>> 48e5775572aa2b3fd1eec29ea8430f131059eebd
    return messages

def sendMessage(senderID, receiverID, content):
    message = Message(senderID=senderID, receiverID=receiverID, content=content)
    db.session.add(message)
    db.session.commit()
