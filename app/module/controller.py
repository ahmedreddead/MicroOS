from flask import render_template, request
from app import app

@app.route('/')
def index():
    return render_template("index.html",title="MicroOs",description="Smart iot solution.")

@app.route('/admin')
def login():
    return render_template("login.html")

@app.errorhandler(404)
def notfound(error):
    return render_template("404.html")