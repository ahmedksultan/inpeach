from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
import sqlite3
import os
import json

app = Flask(__name__)

# setting up the database
DB_FILE = "deutschebank.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False)
c = db.cursor()

@app.route("/")
def root():
    return __name__;

if __name__ == "__main__":
    app.debug = True
    app.run()
