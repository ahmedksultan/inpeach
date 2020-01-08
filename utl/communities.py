from .models import db, Community, Members, User

def getCommunities(userID):
    members = Member.query.filter_by(userID=userID).all()
    communities = []
    for member in members:
        community = Community.query.filter_by(communityID=member.communityID).first()
        communities.append(community)
    return community

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