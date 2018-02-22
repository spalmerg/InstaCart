from flask import render_template, flash, request, redirect
from App import app
from wtforms import validators
from App.forms import OrderForm, FlaskForm
from Develop.Model.model import give_recommendation
import pickle

model = pickle.load(open("Develop/Model/model.pkl", "rb"))
choices = pickle.load(open("Develop/Model/rid_to_name.pkl", "rb"))

@app.route('/', methods=['GET'])
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
  form=OrderForm(request.form)

  if request.method == 'POST':
    item=request.form['item']
    if form.validate():
      neighbors=give_recommendation(model,item,choices)
      return render_template('/thankyou.html', item=neighbors)
    else:
      flash("We don't have that item")
  return render_template('homepage.html', form=form)

@app.route('/thankyou')
def thankyou():
  return render_template('thankyou.html')