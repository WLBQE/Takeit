from flask import render_template, request

from app import app, db
from .forms import LoginForm, RegisterForm, EventDetailForm
from .models import User, Event


@app.route('/')
@app.route('/<user>')
def index(user=None):
    return render_template('index.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return '<h1>' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        if User().create(form.email.data, form.password.data, form.username.data) is not None:
            return '<h1>New user has been created!</h1>'
        return '<h1>Failed to create new user!</h1>'

    return render_template('signup.html', form=form)


@app.route('/profile/<id>')
def profile(id):
    return render_template('profile.html', name=id)


@app.route('/event_detail/<int:id>')
def event_detail(id):
    event = Event(id).find()
    if event is None:
        return '<h1>404 NOT FOUND</h1>'
    return '{{event.name}}'
    #return render_template('event_detail.html', event)