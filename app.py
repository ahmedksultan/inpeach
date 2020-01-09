from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from config import Config
from utl import models
db = models.db
from utl import api
from utl import friends as friendsfunctions
from utl import messages as messagesfunctions
from utl import users as usersfunctions

app = Flask(__name__)
app.config.from_object(Config)

@app.route("/")
def root():
    return redirect(url_for('home')) # when login system is in place, will be changed

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("signup.html")

@app.route("/dashboard")
def home():
    return render_template("dashboard.html", user="Ahmed", weather=api.getCurrentWeather())

@app.route("/activity")
def activity():
    return render_template("activity.html", user="Ahmed")

@app.route("/friends")
def friends():
    friendslist = friendsfunctions.getFriends(1)
    return render_template("friends.html", friends=friendslist)

@app.route("/communities")
def communities():
    return render_template("communities.html", user="Ahmed")

@app.route("/messages/")
def messages():
    friendslist = friendsfunctions.getFriends(1)
    return render_template("messages.html", friends=friendslist)

@app.route("/messages/<contactID>")
def chat(contactID):
    contact = usersfunctions.getUser(contactID)
    chat = messagesfunctions.getMessages(1, contactID)
    return render_template("chat.html", userID = 1, contact=contact, messages=chat)

@app.route("/sendmessage/<contactID>", methods=["POST"])
def sendmessage(contactID):
    content = request.form['content']
    messagesfunctions.sendMessage(1, contactID, content)
    return redirect(url_for('chat', contactID=contactID))

if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.debug = True
    app.run()
