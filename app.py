from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from config import Config
from utl import models
db = models.db
Community = models.Community
from utl import functions
import sqlite3
import os

app = Flask(__name__)
app.config.from_object(Config)

@app.route("/")
def root():
    newcommunity = Community(name="name", description="description")
    db.session.add(newcommunity)
    newcommunity2 = Community(name="name2", description="description2")
    db.session.add(newcommunity2)
    db.session.commit()
    return __name__

@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.debug = True
    app.run()
