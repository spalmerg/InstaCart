import psycopg2
import pandas as pd
import os
import pickle
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

choices = pickle.load(open("analyze/models/rid_to_name.pkl", "rb")).items()

class OrderForm(FlaskForm):
  item = SelectField(label='Pick something tasty', choices=choices)
  submit = SubmitField('Add to cart')

class RecommendForm(FlaskForm):
  item = SelectField(label='Would you also like to buy')
  yes = SubmitField('Yes')
  no = SubmitField('No, Add New Item')
  
  def set_choices(self, recs):
    self.item.choices = recs

class FinalForm(FlaskForm):
  item=SelectField(label="Your order includes:")
  
  def set_choices(self, recs):
    self.item.choices = recs
