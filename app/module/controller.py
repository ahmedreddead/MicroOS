from flask import render_template, request
from app import app

@app.route('/')
def index():
    return render_template("index.html",title="MicroOs",description="Smart iot solution.")

@app.route('/admin')
def login():
    return render_template("login.html")

@app.route('/video')
def video():
    return render_template("video.html")
@app.route('/camera')
def camera():
    return render_template("camera.html")
@app.errorhandler(404)
def notfound(error):
    return render_template("404.html")