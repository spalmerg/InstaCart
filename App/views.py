from flask import render_template, flash, request, redirect, url_for
from App import app
from wtforms import validators
from App.forms import OrderForm, FlaskForm, RecommendForm
from analyze.src.models.model import give_recommendation
import pickle
import ast

model = pickle.load(open("analyze/models/model.pkl", "rb"))
choices = pickle.load(open("analyze/models/rid_to_name.pkl", "rb"))

@app.route('/', methods=['GET'])
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
  form=OrderForm()

  if request.method == 'POST':
    item=request.form['item']
    if form.validate():
      neighbors=give_recommendation(model,item,choices)
      return redirect(url_for('thankyou', item=choices[item], recs=neighbors))
    else:
      flash("We don't have that item")
  return render_template('homepage.html', form=form)


@app.route('/thankyou', methods=['GET', 'POST'])
def thankyou():
  #declare recommender form
  rec_form=RecommendForm()

  if request.method == 'GET':
    #get item ordered from homepage
    item = request.args.get('item')
  
    #get recommendations generated
    temp = request.args.get('recs')
  
    # translate recommendations to dictionary for new form
    temp = ast.literal_eval(temp)
    rec_form.set_choices(temp.items())
  if request.method == 'POST':
    return redirect(url_for('homepage'))

  #display new page and custom form and heading
  return render_template('thankyou.html', form=rec_form, item=item)