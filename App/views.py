from flask import render_template, request, redirect, url_for, session
from App import app
from App.forms import OrderForm, RecommendForm, FinalForm
from analyze.src.models.model import give_recommendation
import pickle
import ast
from create_db import add_order

model = pickle.load(open("analyze/models/model.pkl", "rb"))
choices = pickle.load(open("analyze/models/rid_to_name.pkl", "rb"))

@app.route('/', methods=['GET'])
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
  form=OrderForm()
  try:
    if request.method == 'POST':
      item=request.form['item']
      session[item] = False
      neighbors=give_recommendation(model,item,choices)
      return redirect(url_for('rec', item=choices[item], recs=neighbors))
  except: 
    pass
  return render_template('homepage.html', form=form)


@app.route('/rec', methods=['GET', 'POST'])
def rec():
  #declare recommender form
  rec_form=RecommendForm()

  if request.method == 'GET':
    #get item ordered from homepage
    item = request.args.get('item')
    #get generated recommendations
    temp = request.args.get('recs')
    # translate recommendations to dictionary for new form
    temp = ast.literal_eval(temp)
    rec_form.set_choices(temp.items())
  
  if request.method == 'POST':
    if 'yes' in request.form:
      rec=request.form['item']
      session[rec] = True
      return redirect(url_for('homepage'))
    if 'no' in request.form:
      return redirect(url_for('homepage'))

  #display new page and custom form and heading
  return render_template('rec.html', form=rec_form, item=item)

@app.route('/thankyou', methods=['GET'])
def thankyou():
  form=FinalForm()
  order = {}
  try:
    del session["csrf_token"]
    for id in session.keys():
      order[id] = choices[id]
    add_order(session)
    session.clear()
  except:
    pass
  form.set_choices(order.items())
  return render_template('thankyou.html', form=form)


