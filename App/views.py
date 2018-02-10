from flask import render_template, flash, request, redirect
from App import app
from wtforms import StringField, validators
from App.forms import OrderForm, FlaskForm
from model import


@app.route('/', methods=['GET', 'POST'])
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
  form = OrderForm(request.form)
  
  print(form.errors)
  if request.method == 'POST':
    item = request.form['item']

    if form.validate():
      recommendation = item
      return render_template('/thankyou.html', item=item)
    else:
      flash("We don't have that item")
  return render_template('homepage.html', form=form)

@app.route('/thankyou')
def thankyou():
  return render_template('thankyou.html')