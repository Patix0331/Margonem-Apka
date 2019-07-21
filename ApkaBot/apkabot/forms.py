from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, NumberRange, Optional
from apkabot.models import User, Account

class RegistrationForm(FlaskForm):

    username = StringField('Username', validators = [
        DataRequired(),
        Length(min=3, max=15)
        ])

    email = StringField('Email', validators=[
        DataRequired(),
        Email()])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=4,max=30,message=" Hasło powinno mieć od 4 do 30 znaków!")])

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
        Regexp(regex=r'https:\/\/\w\w\w\.margonem\.pl.+profile\D+(\d+)', message="Zły link do profilu"),
        Length(min=42, max=50)])

    referral = IntegerField('Refferal', validators=[Optional(), NumberRange(1,4000, message="")])

    submit = SubmitField('Połącz konto!')



    def validate_referral(self, referral):
        try:
            user = User.query.filter_by(id = referral.data).first()
            if user:
                pass
            else:
                raise ValidationError('Podaj poprawny referral')
        except:
            raise ValidationError('Podaj poprawny referral')

    def validate_profile(self, profile):
        account = Account.query.filter_by(url=profile.data).first()
        if account:
            raise ValidationError('Ten profil jest już połączony!')

class PanelForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired(), NumberRange(1,4000, message="")])

    username = StringField('Username', validators = [
        Optional(),
        Length(min=3, max=15)
        ])

    email = StringField('Email', validators=[
        Optional(),
        Email()])

    password = PasswordField('Password', validators=[Optional()])

    ref = IntegerField('Ref', validators=[Optional()])
    
    submit = SubmitField('Change!')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ten login już jest zajęty!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ten email już jest zajęty!')

    def validate_id(self, id):
        user = User.query.filter_by(id=id.data).first()
        if not user:
            raise ValidationError('Nie ma użytkownika o podanym ID!')

class AddLicense(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired(), NumberRange(1,4000, message="")])

    howLong = SelectField(u'Na ile?', choices=[("0.04166", 'Godzina'),("0.5", 'Pół dnia'),("1", 'Dzień'), ("7", 'Tydzien'), ("15", 'Pół miesiąca'), ("30", 'Miesiąc')])

    submit = SubmitField('Nadaj!')

    def validate_id(self, id):
        acc = Account.query.filter_by(id=id.data).first()
        if not acc:
            raise ValidationError('Nie ma użytkownika o podanym ID!')

class PlayBot(FlaskForm):
    login = StringField("Login", validators=[DataRequired(), Length(min=3,max=20,message="Login musi mieć od 3 do 20 znaków!")])
    password = PasswordField("Hasło", validators=[DataRequired(), Length(min=4,max=20,message="Login musi mieć od 6 do 20 znaków!")])

class SendChars(FlaskForm):
    chars = SelectField('Postacie', choices=[])
    maps = SelectField('Mapy', choices=[('2675', 'Leśny Gąszcz [1-5]'), ('2676', 'Zaginiony Matecznik [6-10]')])
    add = SubmitField('Dodaj postać')
    submit = SubmitField('Start!')