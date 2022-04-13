from tokenize import String
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField
from wtforms_sqlalchemy.orm import model_form, QuerySelectField
from wtforms.validators import DataRequired, Length, URL
from grocery_app.models import GroceryStore, ItemCategory

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""
    title = StringField('Store Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    address = StringField('Store Address',
        validators=[Length(min=3, max=110)])
    submit = SubmitField('Add New Store')

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""
    name = StringField('Product Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    price = FloatField('Product Price',
        validators=[DataRequired()])
    category = SelectField('Product Category', choices=ItemCategory.choices())
    photo_url = StringField('Product Photo URL')
    store = QuerySelectField('Store',
        query_factory=lambda: GroceryStore.query, allow_blank=False)
    submit = SubmitField('Add New Product')
