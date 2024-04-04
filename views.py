from flask import Blueprint, render_template, request, url_for, redirect

views = Blueprint(__name__, "views")

@views.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html", results='')
    else:
        return render_template("index.html", results='something')