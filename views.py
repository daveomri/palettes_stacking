from flask import Blueprint, render_template, request, url_for, redirect

from static.code.solver import PalettesStackingSolver

views = Blueprint(__name__, "views")

@views.route("/", methods=["GET", "POST"])
def home():
  if request.method == "GET":
    
    return render_template("index.html", results='')
  else:
    solver = PalettesStackingSolver(form_to_array(request.form))
    return render_template("index.html", results=solver.run())
      
def form_to_array(form):
  result = []
  for i in range(1, int(((len(form) - 1) / 2) + 1)):
    result.append([
      int(form.get('palette-{}-left'.format(i))),
      int(form.get('palette-{}-right'.format(i)))])
    
  return result