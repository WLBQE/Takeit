from flask import render_template
from flask_bootstrap import Bootstrap
from app import app, db
from .forms import LoginForm
from .forms import RegisterForm
from .models import User


@app.route('/')
@app.route('/<user>')
def index(user=None):
    return render_template('index.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
    #     hashed_password = generate_password_hash(form.password.data, method='sha256')
    #     new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    #     db.session.add(new_user)
    #     db.session.commit()
        return '<h1>New user has been created!</h1>'

    return render_template('signup.html', form=form)


@app.route('/profile/<name>')
def profile(name):
    return render_template('profile.html', name = name)


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/event_detail')
def event_detail():
    return render_template('event_detail.html')