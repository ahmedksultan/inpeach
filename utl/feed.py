from .models import db, User, Community, Post, Member

def getPosts(userID):
    communities = Member.query.filter_by(userID=userID).all()
    communityID = []
    for community in communities:
        communityID.append(community.communityID)
    posts = Post.query.filter_by(communityID=1).all()
    return posts