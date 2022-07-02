from flask import render_template, url_for, redirect, flash
from gol_app import app, bcrypt, db
from gol_app.forms import SignUp, LogIn
from gol_app.models import User, Scores
from flask_login import current_user, login_user, logout_user
from datetime import datetime



@app.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('index.html')
    return redirect(url_for('log_in'))


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def log_in():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    login_form = LogIn()
    if login_form.validate_on_submit():
        user = User.user_in_database(login_form.username.data)
        print(bool(user))
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember.data)
            return redirect(url_for('home'))
        elif user and not bcrypt.check_password_hash(user.password, login_form.password.data):
            flash('Invalid password', 'warning')
            return redirect(url_for('log_in'))
        else:
            flash('There is no such user, you need to sign up first.', 'warning')
            return redirect(url_for('log_in'))
    return render_template('login.html', form=login_form)


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    signup_form = SignUp()
    if signup_form.validate_on_submit():
        if signup_form.password.data != signup_form.password_again.data:
            flash("Passwords don't match.", 'danger')
            return redirect(url_for('sign_up'))
        else:
            new_user = User(
                username=signup_form.username.data,
                password=bcrypt.generate_password_hash(signup_form.password.data).decode('utf-8'),
                email=signup_form.email.data,
                about=signup_form.about.data,
            )
            new_user.save_in_db()
            return redirect(url_for('log_in'))
    return render_template('signup.html', form=signup_form)


@app.route('/account')
def account():
    if current_user.is_authenticated:
        return render_template('account.html')
    return redirect(url_for('log_in'))


@app.route('/logout')
def log_out():
    logout_user()
    return redirect(url_for('log_in'))


@app.route('/save_score/<string:score>')
def save_score(score):
    if current_user.is_authenticated:
        flash('Score added to your account', 'success alert-sm')
        s = Scores(score=score, user_id=current_user, date=datetime.now().strftime('%y/%m/%d %H:%M:%S'))
        current_user.scores.append(s)
        db.session.commit()
        return redirect(url_for('home'))
    return redirect(url_for('log_in'))
