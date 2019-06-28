from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from apkabot.models import User, Account
from random import randint
class RegistrationForm(FlaskForm):

    username = StringField('Username', validators = [
        DataRequired(),
        Length(min=3, max=15)
        ])

    email = StringField('Email', validators=[
        DataRequired(),
        Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ten login już jest zajęty!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ten email już jest zajęty!')

class LoginForm(FlaskForm):

    email = StringField('Email', validators=[
        DataRequired(),
        Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Sign Up')

class ConnectAccountForm(FlaskForm):
    profile = StringField('Link do profilu', validators=[
        DataRequired(),
        Regexp(regex=r'^https:\/\/www.margonem.pl\/\?task=profile\&id=[0-9]([0-9])*$', message="Zły link do profilu"),
        Length(min=42, max=50)])
        
    submit = SubmitField('Połącz konto!')

    def validate_profile(self, profile):
        account = Account.query.filter_by(url=profile.data).first()
        if account:
            raise ValidationError('Ten profil jest już połączony!')