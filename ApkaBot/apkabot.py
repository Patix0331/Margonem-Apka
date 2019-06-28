from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ab3cd3d7254a2d2a258e08ef01b4ae71'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    accounts = db.relationship('Account', backref='owner', lazy=True)

    def __repr__(self):
        return f"User('{self.id}','{self.username}', '{self.email}')"

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(30), nullable=True)
    url = db.Column(db.String(50), nullable=False)
    license = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Account('owner:{self.user_id}', '{self.id}', '{self.url}'"

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title="Home Page")

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f'{form.username.data} udało Ci się stworzyć konto! ', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title="Rejestracja", form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data  == 'password':
            flash('Zalogowaleś się na swoje konto!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Złe hasło lub email!', 'danger')

    return render_template('login.html', title="Logowanie", form=form)

if __name__ == "__main__":
    app.run(debug=True)