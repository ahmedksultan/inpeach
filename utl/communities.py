from .models import db, Community, Member, User

def getCommunityByName(name):
    community = Community.query.filter_by(name=name).first()
    return community

def getCommunities(userID):
    members = Member.query.filter_by(userID=userID).all()
    communities = []
    for member in members:
        community = Community.query.filter_by(communityID=member.communityID).first()
        communities.append(community)
    return community

def inCommunity(userID, communityID):
    members = Member.query.filter_by(userID=userID).all()
    for member in members:
        if(member.communityID == communityID):
            return True
    False

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
