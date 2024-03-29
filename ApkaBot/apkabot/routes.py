from flask import render_template, url_for, flash, redirect, request, session
from apkabot import app, db, bcrypt
from apkabot.forms import RegistrationForm, LoginForm, ConnectAccountForm, PanelForm, AddLicense, PlayBot, SendChars
from apkabot.models import User, Account
from apkabot.bot.apka import Account as ac
from flask_login import login_user, current_user, logout_user, login_required
from requests import get, post

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('acc'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data, 
            email=form.email.data, 
            password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('{} udało Ci się stworzyć konto! '.format(form.username.data), 'success')
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

            # if form.referral.data is not:
            #     referral = 1

            account = Account(
                owner_id = current_user.id,
                user_id = user_id,
                url = form.profile.data,
                ref = form.referral.data)
            db.session.add(account)
            db.session.commit()

            flash("Konto zostało połączone!","success")
            return redirect(url_for('acc'))

    #acc_list = current_user.
    return render_template('account.html', acc_list = acc_list, auth=auth, title='{}'.format(current_user.username), form=form)
    

@app.route("/panel", methods=['GET','POST'])
@login_required
def panel():
    
    #redirect if not admin
    if current_user.id != 1 or current_user.id != 2:
        return redirect(url_for('acc')) 

    form = PanelForm()
    form2 = AddLicense(howLong="30")
    acc_list = User.query.all()
    mAcc_list = Account.query.all()

    # if form.validate_on_submit():
    #     user = User.query.filter_by(id=form.id.data).first()

    if form2.validate_on_submit():
        from datetime import datetime, timedelta

        acc = Account.query.filter_by(id=form2.id.data).first()

        lic = form2.howLong.data

        if datetime.now() > acc.license:
            acc.license = datetime.utcnow() + timedelta(days = float(lic))
        else:
            acc.license = acc.license + timedelta(days = float(lic))

        if acc.ref:
            if lic == "7":
                free = 0.5
            elif lic == "15":
                free = 1
            elif lic == "30":
                free = 2
            else:
                free = 0

            user = User.query.filter_by(id = acc.ref).first()
            user.free = user.free + free

        db.session.commit()
        

        flash("Nadano {} licencji na konto {}a".format(lic, form2.id.data), "success")
        return redirect(url_for('panel'))

    return render_template('panel.html', acc_list = acc_list, mAcc_list=mAcc_list, title='Panel', form=form, form2=form2)

@app.route("/play", methods=['GET','POST'])
@login_required
def play():

    from datetime import datetime

    form = PlayBot()

    if form.validate_on_submit():

        apka = ac(form.login.data, form.password.data)
        apka.signIn()

        if not apka.cookies:

            flash("Złe hasło lub login do konta margonem!", "danger")
            return redirect(url_for("play"))

        acc = Account.query.filter_by(user_id=apka.cookies["user_id"]).first()

        if acc:
            
            acc.login=str(form.login.data)
            acc.password=str(form.password.data)
            db.session.commit()

            if acc.license > datetime.now():

                #chars = [(chars.index(c), "{} - {} lvl, {}".format(c[1], c[2], c[4])) for c in chars]
                session['asd'] = str(form.login.data)
                session['dsa'] = str(form.password.data)
                session['license_time'] = acc.license
                session['verified'] = True

                try:
                    session.pop('selected_chars')
                except KeyError:
                    pass

                return redirect(url_for('bot'))

            else:

                flash("Przedawniona licencja!", "danger")  
                redirect(url_for("play"))

        else:

            flash("Połącz konto i kup licencje!", "danger")
            redirect(url_for("acc"))


    return render_template('margoLogin.html', title="Bot", form=form)

@app.route("/bot", methods=['GET','POST'])
@login_required
def bot():

    try:
        session.get('verified', None)
    except NameError:
        return redirect(url_for('play'))

    form = SendChars()
    
    apka = ac(session.get('asd', None), session.get('dsa', None))
    apka.signIn()
    apka.get_chars()

    chars = [(char, '{} - {} lvl, {}'.format(
        apka.characters[char]['nick'], 
        apka.characters[char]['lvl'], 
        apka.characters[char]['world'])) for char in apka.characters]

    form.chars.choices = chars

    if form.validate_on_submit():

        selected_chars = session.get('selected_chars', None)

        if form.submit.data:
            
            flash("Bot wystartował {}!".format(selected_chars), 'success')
            apka.run(selected_chars, session.get('license_time', None))

        elif form.add.data:

            if not selected_chars:
                selected_chars = dict()

            selected_chars[form.chars.data] = {'map' : form.maps.data}
            session['selected_chars'] = selected_chars

    return render_template('logged.html', title="Zalogowany", form=form)