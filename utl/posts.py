from .models import db, Post

def getUserPosts(userID):
    posts = Post.query.filter_by(communityID=NULL, userID=userID)
    return posts

def getCommunityPosts(communityID):
    posts = Post.query.filter_by(commmunityID=communityID)
    return posts

def createPost(communityID, userID, title, content):
    if communityID == None:
        post = Post(userID=userID, title=title, content=content)
    else:
        post = Post(communityID=communityID, userID=userID, title=title, content=content)
    db.session.add(post)
    db.session.commit()

def deletePost(postID):
    Post.query.filter_by(postID=postID).first().delete()
    db.session.commit()order_by