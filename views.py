from flask import Blueprint, render_template, request, url_for, redirect

from static.code.solver import PalletsStackingSolver

views = Blueprint(__name__, "views")

@views.route("/", methods=["GET", "POST"])
def home():
  if request.method == "GET":
    
    return render_template("index.html", hasResults=False)
  else:
    form_arr = form_to_array(request.form)
    solver = PalletsStackingSolver(form_arr)
    result, length = solver.run()
    return render_template("index.html", hasResults=True, results=result, length=length, form_arr=form_arr)
      
def form_to_array(form):
  result = []
  print(form)
  for i in range(1, int(((len(form) - 1) / 3) + 1)):
    for _ in range(0, int(form.get('pallet-{}-count'.format(i)))):
      result.append([
        int(form.get('pallet-{}-left'.format(i))),
        int(form.get('pallet-{}-right'.format(i)))])
    
  return result