from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from config import Config
from utl import models
db = models.db
Group = models.Group
import sqlite3
import os

app = Flask(__name__)
app.config.from_object(Config)

@app.route("/")
def root():
    newgroup = Group(name="name", description="description")
    db.session.add(newgroup)
    newgroup2 = Group(name="name2", description="description2")
    db.session.add(newgroup2)
    db.session.commit
    return __name__;

if __name__ == "__main__":
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.debug = True
    app.run()
