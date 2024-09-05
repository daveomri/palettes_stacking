from flask import Blueprint, render_template, request, url_for, redirect

from static.code.solver import PalletsStackingSolver

views = Blueprint(__name__, "views")

@views.route("/", methods=["GET", "POST"])
def home():
  if request.method == "GET":
    return render_template("index.html", hasResults=False)
  else:
    pallets_arr, truck_width = form_to_array(request.form)
    solver = PalletsStackingSolver(pallets_arr, truck_width)
    result, length = solver.run()
    return render_template("index.html", hasResults=True, results=result, length=length, form_arr=pallets_arr, truck_width=truck_width)
      
def form_to_array(form):
  truck_width = int(form.get('truck-width'))
  # get all pallets
  result = []
  for i in range(1, int(((len(form) - 1) / 3) + 1)):
    for _ in range(0, int(form.get('pallet-{}-count'.format(i)))):
      result.append([
        int(form.get('pallet-{}-left'.format(i))),
        int(form.get('pallet-{}-right'.format(i)))])
  return result, truck_width