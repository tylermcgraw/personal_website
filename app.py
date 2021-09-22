from flask import Flask, redirect, render_template 

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")


@app.route("/blog")
def blog():
  return render_template("blog.html")


@app.route("/dashboard")
def dashboard():
  return render_template("dashboard.html")


@app.route("/projects")
def projects():
  return render_template("projects.html")

  