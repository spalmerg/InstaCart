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


@app.route('/', methods=['GET'])
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    # initialize order form
    form = OrderForm()
    # ensure user made a selection (with try block)
    try:
        if request.method == 'POST':
            item = request.form['item']  # retrieve item
            session[item] = {'was_rec': False, 'rec_from': None}  # store info
            session['temp'] = item  # save item name
            neighbors = give_recommendation(model, item, choices)  # make recs
            return redirect(url_for('rec', item=choices[item], recs=neighbors))
    except:
        pass
    return render_template('homepage.html', form=form)


@app.route('/rec', methods=['GET', 'POST'])
def rec():
    rec_form = RecommendForm()  # declare reccomender form
    if request.method == 'GET':  # inbound traffic
        item = request.args.get('item')
        temp = request.args.get('recs')
        temp = ast.literal_eval(temp)
        rec_form.set_choices(temp.items())
    if request.method == 'POST':  # outbound traffic
        if 'yes' in request.form:
            try:
                rec = request.form['item']
                session[rec] = {'was_rec': True, 'rec_from': session['temp']}
            except:
                pass
            return redirect(url_for('homepage'))
        if 'no' in request.form:
            return redirect(url_for('homepage'))
    return render_template('rec.html', form=rec_form, item=item)


@app.route('/thankyou', methods=['GET'])
def thankyou():
    form = FinalForm()  # initialize form
    order = {}  # get ordered items for form
    try:
        del session['csrf_token']
    except:
        pass
    try:
        del session['temp']
    except:
        pass
    for id in session.keys():  # get and set items for form display
        order[id] = choices[id]
    form.set_choices(order.items())
   # add_order(session)  # add order items to db
    session.clear()  # clear session from checkout
    return render_template('thankyou.html', form=form)
