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
    return render_template("feed.html")

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
        return render_template("profile.html", user=user, isFriend=isFriend)

@app.route("/communities")
@login_required
def communities():
    communities = communitiesfunctions.getAllCommunities()
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


@app.route("/joincommunity/<communityID>")
@login_required
def joincommunity(communityID):
    communitiesfunctions.joinCommunity(session['userID'], communityID)
    return redirect(url_for("community", communityID=communityID))

@app.route("/leavecommunity/<communityID>")
@login_required
def leavecommunity(communityID):
    communitiesfunctions.leaveCommunity(session['userID'], communityID)
    return redirect(url_for("communities"))

@app.route("/community/<communityID>")
@login_required
def community(communityID):
    community = communitiesfunctions.getCommunity(communityID)
    incommunity = communitiesfunctions.inCommunity(session['userID'], communityID)
    return render_template("community.html", community = community, incommunity = incommunity)

@app.route("/messages/")
@login_required
def messages():
    friendslist = friendsfunctions.getFriends(session['userID'])
    return render_template("messages.html", friends=friendslist)

@app.route("/messages/<contactID>")
@login_required
def chat(contactID):
    contact = usersfunctions.getUser(contactID)
    chat = messagesfunctions.getMessages(session['userID'], contactID)
    return render_template("chat.html", userID = session['userID'], contact=contact, messages=chat)

@app.route("/sendmessage/<contactID>", methods=["POST"])
@login_required
def sendmessage(contactID):
    content = request.form['content']
    messagesfunctions.sendMessage(session['userID'], contactID, content)
    return redirect(url_for('chat', contactID=contactID))

@app.route("/me")
@login_required
def myfeed():
    user = usersfunctions.getUser(session['userID'])
    return render_template("me.html", user=user)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/register", methods=["POST"])
def register():
    if "userID" in session:
        return redirect(url_for('feed'))
    email = request.form['email']
    pass1 = request.form['password']
    pass2 = request.form['confpassword']
    if usersfunctions.getUserByEmail(email) != None:
        flash("Account with that email already exsists", "error")
        return redirect(url_for('signup'))
    if pass1 != pass2 :
        flash("Passwords do not match", "error")
        return redirect(url_for('signup'))
    flash("Account created successfuly. Please sign in", "success")
    usersfunctions.registerUser(email,pass1,request.form['first'],request.form['last'],request.form['grade'])
    return redirect(url_for('login'))

@app.route("/auth", methods=["POST"])
def auth():
    if "userID" in session:
        flash("You were already logged in, "+session['displayName']+".", "error")
        return redirect(url_for('feed'))
    # information inputted into the form by the user
    user = usersfunctions.getUserByEmail(request.form['email'])
    if user == None: # if email not found
        flash("No user found with given email", "error")
        return redirect(url_for('login'))
    elif request.form['password'] != user.password: # if password is incorrect
        flash("Incorrect password", "error")
        return redirect(url_for('login'))
    else: # hooray! the email and password are both valid
        session['userID'] = user.userID
        session['firstName'] = user.firstName
        session['lastName'] = user.lastName
        session['displayName'] = user.firstName + ' ' + user.lastName
        return redirect(url_for('dashboard'))

@app.route("/logout")
def logout():
    if not "userID" in session:
        flash("Already logged out, no need to log out again", "error")
    else:
        session.pop('userID')
        session.pop('firstName')
        session.pop('lastName')
        session.pop('displayName')
        flash("Successfuly logged out", "success")
    return redirect(url_for('root')) # should redirect back to login

if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.debug = True
    app.run()
