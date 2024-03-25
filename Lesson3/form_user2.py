from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, DateField, widgets, BooleanField
from wtforms.validators import DataRequired, EqualTo, Email, Length


class CheckboxField(BooleanField):
    widget = widgets.CheckboxInput()


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    birthday = DateField('Birthday', format='%Y-%m-%d')
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    agreement = CheckboxField('Согласен', validators=[DataRequired()])
