from .models import db, User, Community, Member, Post, Comment, FriendRequest, Friend, Message

def registerUser(email, password, firstName, lastName, grade):
    user = User(email=email, password=password, firstName=firstName, lastName=lastName, grade=grade)
    db.session.add(user)
    db.session.commit()

def authenticateUser(email, password):
    user = User.query.filter_by(email=email, password=password).first()
    if user == None:
        return False
    return True

def createCommunity(name, description):
    community = Community(name=name, description=description)
    db.session.add(community)
    db.session.commit()

def joinCommunity(userID, communityID):
    user = User.query.filter_by(userID=userID).first()
    member = Member(communityID=communityID, userID=userID, displayName=user.displayName)
    db.session.add(member)
    db.session.commit()

def leaveCommunity(userID, communityID):
    Member.query.filter_by(communityID=communityID, userID=userID).first().delete()
    db.session.commit()

def getFriendRequests(userID):
    friendrequests = FriendRequest.query.filter_by(receiverID=userID).order_by(FriendRequest.timestamp.desc())
    return friendrequests

def sendFriendRequest(senderID, receiverID, message):
    friendrequest = FriendRequest(senderID=senderID, receiverID=receiverID, message=message)
    db.session.add(friendrequest)
    db.session.commit()

def acceptFriendRequest(requestID):
    friendrequest = FriendRequest.query.filter_by(requestID=requestID).first()
    if friendrequest == None:
        return False
    user = User.query.filter_by(userID=friendrequest.receiverID).first()
    frienduser = User.query.filter_by(userID=friendrequest.senderID).first()
    friend1 = Friend(userID=user.userID, friendID=frienduser.userID, displayName=frienduser.displayName)
    friend2 = Friend(userID=frienduser.userID, friendID=user.userID, displayName=user.displayName)
    db.session.delete(friendrequest)
    db.session.add(friend1)
    db.session.add(friend2)
    db.session.commit()
    return True

def rejectFriendRequest(requestID):
    friendrequest = FriendRequest.query.filter_by(requestID=requestID).first()
    if friendrequest == None:
        return False
    db.session.delete(friendrequest)
    db.session.commit()
    return True