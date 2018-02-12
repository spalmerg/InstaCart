from flask import render_template, flash, request, redirect
from App import app
from wtforms import StringField, validators
from App.forms import OrderForm, FlaskForm
import pickle

model = pickle.load(open("App/model.pkl", "rb"))

@app.route('/', methods=['GET', 'POST'])
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
  form = OrderForm(request.form)
  
  print(form.errors)
  if request.method == 'POST':
    item = request.form['item']

    if form.validate():
      neighbors = model.get_neighbors(int(item),5)
      neighbors = [model.trainset.to_raw_iid(inner_id) for inner_id in neighbors]
      return render_template('/thankyou.html', item=neighbors)
    else:
      flash("We don't have that item")
  return render_template('homepage.html', form=form)

@app.route('/thankyou')
def thankyou():
  return render_template('thankyou.html')