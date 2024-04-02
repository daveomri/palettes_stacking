from flask import Blueprint, render_template, request, url_for, redirect

views = Blueprint(__name__, "views")

@views.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    else:
        return "Wrong wrong my dear"

@views.route("/results", methods=["POST"])
def results():
    if request.method == "POST":
        return render_template("results.html", plan=request.form["palettes"])
    else:
        return "There is nothing"