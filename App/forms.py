import pickle
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

# load items in recommender for OrderForm
choices = pickle.load(open("analyze/models/rid_to_name.pkl", "rb")).items()


class OrderForm(FlaskForm):  # OrderForm for homepage
    item = SelectField(label='Pick something tasty', choices=choices)
    submit = SubmitField('Add to cart')


class RecommendForm(FlaskForm):  # RecommendForm for recommendation page
    item = SelectField(label='Would you also like to buy')
    yes = SubmitField('Yes')
    no = SubmitField('No, Add New Item')

    def set_choices(self, recs):  # function to set selection
        self.item.choices = recs


class FinalForm(FlaskForm):  # FinalForm to display items in cart
    item = SelectField(label="Your order includes:")

    def set_choices(self, recs):  # function to set selection
        self.item.choices = recs
