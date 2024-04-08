from flask import Blueprint, render_template, request, url_for, redirect

from static.code.solver import PalettesStackingSolver

views = Blueprint(__name__, "views")

@views.route("/", methods=["GET", "POST"])
def home():
  if request.method == "GET":
    
    return render_template("index.html", hasResults=False)
  else:
    form_arr = form_to_array(request.form)
    solver = PalettesStackingSolver(form_arr)
    result, length = solver.run()
    return render_template("index.html", hasResults=True, results=result, length=length, form_arr=form_arr)
      
def form_to_array(form):
  result = []
  for i in range(1, int(((len(form) - 1) / 2) + 1)):
    result.append([
      int(form.get('palette-{}-left'.format(i))),
      int(form.get('palette-{}-right'.format(i)))])
    
  return result