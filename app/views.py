from flask import render_template, request, redirect, session, abort
import sys
from app import app, db
from .forms import LoginForm, RegisterForm, EventDetailForm
from .models import User, Event


@app.route('/')
@app.route('/<username>')
def index(username=None):
    if 'username' in session:
        if session['username'] == username:
            return render_template('index.html', user=username)
    return "You are not logged in <br><a href = '/login'></b>" + \
        "click here to log in</b></a>"


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = User().authenticate(form.email.data, form.password.data)
        if username is not None:
            session['username'] = username
            return redirect('/%s' % username)
        else:
            return redirect('/login')

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        if User().create(form.email.data, form.password.data, form.username.data) is not None:
            username = form.username.data
            session['username'] = username
            return redirect('/%s' % username)
        return "User exist! <br><a href = '/signup'></b>" + \
               "click here to sign up again</b></a>"

    return render_template('signup.html', form=form)


@app.route('/profile/<id>')
def profile(id):
    return render_template('profile.html', name=id)


@app.route('/event_detail/<int:id>')
def event_detail(id):
    event = Event(id).find()
    if event is None:
        return abort(404)
    return '{{event.name}}'
    #return render_template('event_detail.html', event)