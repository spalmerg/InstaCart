from flask import render_template, request, redirect, url_for, session
from App import app
from App.forms import OrderForm, RecommendForm, FinalForm
from analyze.src.models.model import give_recommendation
import pickle
import ast
from create_db import add_order

# load the recommender model
model = pickle.load(open("analyze/models/model.pkl", "rb"))
# load the id : item key
choices = pickle.load(open("analyze/models/rid_to_name.pkl", "rb"))

#homepage
@app.route('/', methods=['GET'])
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
  # initialize order form
  form=OrderForm()
  # ensure user made a selection (with try block)
  try:
    if request.method == 'POST':
      item=request.form['item'] #retrieve item
      session[item] = {'was_rec':False, 'rec_from':None} #save db info
      session['temp'] = item #save item name
      neighbors=give_recommendation(model,item,choices) #make recommendations
      return redirect(url_for('rec', item=choices[item], recs=neighbors)) #redirect
  except: 
    pass
  return render_template('homepage.html', form=form)


@app.route('/rec', methods=['GET', 'POST'])
def rec():
  #declare recommender form
  rec_form=RecommendForm()
  #inbound traffic
  if request.method == 'GET':
    #get item ordered from homepage
    item = request.args.get('item')
    #get generated recommendations
    temp = request.args.get('recs')
    # translate recommendations to dictionary for new form
    temp = ast.literal_eval(temp)
    rec_form.set_choices(temp.items())
  #exiting traffic
  if request.method == 'POST':
    #if they say they want something, make sure they selected an item
    if 'yes' in request.form:
      try:
        rec=request.form['item']
        session[rec] = {'was_rec':True, 'rec_from':session['temp']}
      except:
        pass
      # if they didn't, return them home
      return redirect(url_for('homepage'))
    # redirect home if they don't like the recommendations
    if 'no' in request.form:
      return redirect(url_for('homepage'))
  #display new page and custom form and heading
  return render_template('rec.html', form=rec_form, item=item)

@app.route('/thankyou', methods=['GET'])
def thankyou():
  #set up final form to display ordered items
  form=FinalForm()
  # get names for order to display
  order = {}
  # delete unnecessary session items
  try:
    del session['csrf_token']
  except:
    pass
  try:
    del session['temp']
  except:
    pass
  #get and set items for form display
  for id in session.keys():
    order[id] = choices[id]
  form.set_choices(order.items())
  #add order items to db
  add_order(session)
  #clear session from checkout
  session.clear()
  return render_template('thankyou.html', form=form)


