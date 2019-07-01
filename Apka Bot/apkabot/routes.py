from flask import render_template, url_for, flash, redirect, request
from apkabot import app, db, bcrypt
from apkabot.forms import RegistrationForm, LoginForm, ConnectAccountForm
from apkabot.models import User, Account
from flask_login import login_user, current_user, logout_user, login_required
from requests import get
from bot import StartBot

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data, 
            email=form.email.data, 
            password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.username.data} udało Ci się stworzyć konto! ', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title="Rejestracja", form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('acc'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('acc'))
        else:
            flash('Zły email lub hasło!', 'danger')

    return render_template('login.html', title="Logowanie", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/acc", methods=['GET','POST'])
@login_required
def acc():
    form = ConnectAccountForm()
    auth = current_user.password[30:-10]
    
    acc_list = Account.query.filter_by(owner_id = current_user.id)

    if form.validate_on_submit():

        data = get(form.profile.data)

        if data.text.find(auth) == -1:
            print(data.text.find(auth))
            print(auth)
            flash("Na profilu nie znaleziono kodu weryfikującego!", "danger")
            return redirect(url_for('acc'))
        else:
            user_id = form.profile.data[41:]
            account = Account(
                owner_id = current_user.id,
                user_id = user_id,
                url = form.profile.data)
            db.session.add(account)
            db.session.commit()

            flash("Konto zostało połączone!","success")
            return redirect(url_for('acc'))

    #acc_list = current_user.
    return render_template('account.html', acc_list = acc_list, auth=auth, title=f'{current_user.username}', form=form)
