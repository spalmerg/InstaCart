import psycopg2
import pandas as pd
import os
import pickle
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

choices = pickle.load(open("Develop/Model/rid_to_name.pkl", "rb")).items()

class OrderForm(FlaskForm):
 item = SelectField(label='Item', choices=choices)
 submit = SubmitField('Add to cart')