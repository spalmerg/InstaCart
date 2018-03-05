import psycopg2
import pandas as pd
import os
import pickle
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

# load items in recommender for OrderForm
choices = pickle.load(open("analyze/models/rid_to_name.pkl", "rb")).items()

# OrderForm for homepage
class OrderForm(FlaskForm):
  item = SelectField(label='Pick something tasty', choices=choices)
  submit = SubmitField('Add to cart')

# RecommendForm for recommendation page
class RecommendForm(FlaskForm):
  item = SelectField(label='Would you also like to buy')
  yes = SubmitField('Yes')
  no = SubmitField('No, Add New Item')
  
  #function to set recommendation selection
  def set_choices(self, recs):
    self.item.choices = recs

# Final Form to display items in cart
class FinalForm(FlaskForm):
  item=SelectField(label="Your order includes:")
  
  #function to display items in cart
  def set_choices(self, recs):
    self.item.choices = recs
