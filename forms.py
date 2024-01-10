from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FileField, FloatField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange

from models import User


def validate_username(username):
    user = User.query.filter_by(username=username.data).first()
    if user:
        raise ValidationError('That username is already taken. Please choose a different one.')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = StringField('Role(default = GUEST')

    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

class AddProductForm(FlaskForm):
    category = StringField("Category", validators=[DataRequired()])
    name = StringField("product name", validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()])
    img = FileField("Picture ", validators=[DataRequired()])

    submit = SubmitField("Submit")

class EditItemForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired(), Length(min=2, max=50)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Update')