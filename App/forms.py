from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class OrderForm(FlaskForm):
  item = StringField('Item', validators=[DataRequired()])
  submit = SubmitField('Add to cart')