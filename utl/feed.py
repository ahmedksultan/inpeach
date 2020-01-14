from .models import db, User, Community, Post, Member

def getPosts(userID):
    members = Member.query.filter_by(userID=userID).all()
    communityID = []
    for member in members:
        communityID.append(member.communityID)
    posts = Post.query.filter(Post.communityID.in_(communityID)).order_by(Post.timestamp.desc())
    return posts