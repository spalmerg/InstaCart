import psycopg2
import pandas as pd
import os
import pickle
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

choices = pickle.load(open("analyze/models/rid_to_name.pkl", "rb")).items()

class OrderForm(FlaskForm):
  item = SelectField(label='What would you like to buy?', choices=choices)
  submit = SubmitField('Add to cart')


class RecommendForm(FlaskForm):
  item=SelectField(label='Would you also like to buy')
  submit = SubmitField("MEOW WOOF MOO")
  #yes = SubmitField('Yes')
  #no = SubmitField('No, Add New Item')
  
  def set_choices(self, recs):
    self.item.choices = recs
