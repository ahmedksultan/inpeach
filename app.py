from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from config import Config
from utl import api, models, messages, comments, communities, friends, posts, users
db = models.db
app = Flask(__name__)
app.config.from_object(Config)

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
        return redirect(url_for('feed'))
    else:
        return redirect(url_for('login'))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=session['username'], weather=api.getCurrentWeather())

@app.route("/feed")
@login_required
def activity():
    return render_template("feed.html", user=session['username'])

@app.route("/friends")
@login_required
def friends():
    return render_template("friends.html", user=session['username'])

@app.route("/communities")
@login_required
def communities():
    return render_template("communities.html", user=session['username'])

@app.route("/messages")
@login_required
def messages():
    return "Work in progress!"

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
    pass2 = request.form['password2']
    fname = request.form['first']
    lname = request.form['last']
    grade = request.form['grade']
    if pass1 != pass2 :
        flash("Passwords do not match", "error")
        return redirect(url_for('signup'))
    users.registerUser()
    return redirect(url_for('login'))

@app.route("/auth", methods=["POST"])
def auth():
    if "userID" in session:
        flash("You were already logged in, "+session['username']+".", "error")
        return redirect(url_for('feed'))
    # information inputted into the form by the user
    email = request.form['email']
    password = request.form['password']
    user = users.getUser(email)

    if user == None: # if username not found
        flash("No user found with given username", "error")
        return redirect(url_for('login'))
    elif password != user.password: # if password is incorrect
        flash("Incorrect password", "error")
        return redirect(url_for('login'))
    else: # hooray! the username and password are both valid
        session['userID'] = user.userID
        session['username'] = username
        flash("Welcome " + username + ". You have been logged in successfully.", "success")
        return redirect(url_for('dashboard'))

@app.route("/logout")
def logout():
    if not "userID" in session:
        flash("Already logged out, no need to log out again", "error")
    else:
        session.pop('userID')
        session.pop('username')
        flash("Successfuly logged out", "success")
    return redirect(url_for('root')) # should redirect back to login

if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.debug = True
    app.run()
