from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from config import Config
from utl import models, comments, posts
from utl import api
from utl import communities as communitiesfunctions
from utl import friends as friendsfunctions
from utl import messages as messagesfunctions
from utl import users as usersfunctions
from utl import posts as postsfunctions
from utl import comments as commentsfunctions
from utl import feed as feedfunctions
import os


db = models.db
app = Flask(__name__)
app.config.from_object(Config)
#creates secret key for sessions
app.secret_key = os.urandom(32)

#decorator that redirects user to login page if not logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "userID" not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def root():
    if "userID" in session:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route("/dashboard")
@login_required
def dashboard():
    news = api.getNewsArticles()
    if news == "Invalid API Key":
        return render_template("error.html", error=news)
    return render_template("dashboard.html",
        user=session['firstName'],
        weather=api.getCurrentWeather(),
        news=news)

@app.route("/feed")
@login_required
def feed():
    post_data = feedfunctions.getPosts(session['userID'])
    posts = {}
    for post in post_data:
        posts[post] = postsfunctions.getCreator(post.postID)
    return render_template("feed.html", posts=posts)

@app.route("/friends")
@login_required
def friends():
    userID = session['userID']
    friendslist = friendsfunctions.getFriends(userID)
    users = []
    for friend in friendslist:
        users.append(usersfunctions.getUser(friend.friendID))
    reqs = friendsfunctions.getFriendRequests(userID)
    friendrequests = {}
    for req in reqs:
        friendrequests[req] = usersfunctions.getUser(req.senderID)
    preqs = friendsfunctions.getPendingFriendRequests(userID)
    pendingfriendrequests = {}
    for preq in preqs:
        pendingfriendrequests[preq] = usersfunctions.getUser(preq.receiverID)
    print(pendingfriendrequests)
    return render_template("friends.html", users=users, friendrequests=friendrequests, pendingfriendrequests=pendingfriendrequests)

@app.route("/searchfriends", methods=["POST"])
@login_required
def searchfriends():
    userID = session['userID']
    query = request.form['query']
    users = usersfunctions.searchUsers(query)
    reqs = friendsfunctions.getFriendRequests(userID)
    friendrequests = {}
    for req in reqs:
        friendrequests[req] = usersfunctions.getUser(req.senderID)
    preqs = friendsfunctions.getPendingFriendRequests(userID)
    pendingfriendrequests = {}
    for preq in preqs:
        pendingfriendrequests[preq] = usersfunctions.getUser(preq.receiverID)
    print(pendingfriendrequests)
    return render_template("friends.html", users=users, friendrequests=friendrequests, pendingfriendrequests=pendingfriendrequests)

@app.route("/allusers")
@login_required
def allusers():
    userID = session['userID']
    users = usersfunctions.getAllUsers()
    reqs = friendsfunctions.getFriendRequests(userID)
    friendrequests = {}
    for req in reqs:
        friendrequests[req] = usersfunctions.getUser(req.senderID)
    preqs = friendsfunctions.getPendingFriendRequests(userID)
    pendingfriendrequests = {}
    for preq in preqs:
        pendingfriendrequests[preq] = usersfunctions.getUser(preq.receiverID)
    print(pendingfriendrequests)
    return render_template("friends.html", users=users, friendrequests=friendrequests, pendingfriendrequests=pendingfriendrequests)

@app.route("/sendfriendrequest/<receiverID>")
@login_required
def sendfriendrequest(receiverID):
    friendsfunctions.sendFriendRequest(session['userID'], receiverID)
    return redirect(url_for('friends'))

@app.route("/acceptfriendrequest/<requestID>")
@login_required
def acceptfriendrequest(requestID):
    friendsfunctions.acceptFriendRequest(requestID)
    return redirect(url_for('friends'))

@app.route("/declinefriendrequest/<requestID>")
@login_required
def declinefriendrequest(requestID):
    friendsfunctions.declineFriendRequest(requestID)
    return redirect(url_for('friends'))

@app.route("/profile/<userID>")
@login_required
def profile(userID):
    currentuserID = session['userID']
    if currentuserID == int(userID):
        return redirect(url_for('myfeed'))
    else:
        user = usersfunctions.getUser(userID)
        isFriend = friendsfunctions.isFriend(currentuserID, userID)
        posts = postsfunctions.getUserPosts(user.userID)
        return render_template("profile.html", user=user, isFriend=isFriend, posts=posts)

@app.route("/communities")
@login_required
def communities():
    community_data = communitiesfunctions.getAllCommunities()
    communities = {}
    for community in community_data:
        if communitiesfunctions.inCommunity(session['userID'], community.communityID):
            communities[community] = True
        else:
            communities[community] = False
    return render_template("communities.html", communities=communities)

@app.route("/newcommunity", methods = ["POST"])
@login_required
def newcommunity():
    userID = session['userID']
    name = request.form['name']
    description = request.form['description']
    if communitiesfunctions.getCommunityByName(name) != None:
        flash('Community with that name already exists', 'error')
        return redirect(url_for("communities"))
    communitiesfunctions.createCommunity(name, description)
    community = communitiesfunctions.getCommunityByName(name)
    communitiesfunctions.joinCommunity(userID, community.communityID)
    return redirect(url_for('community', communityID = community.communityID))
