from flask import render_template, request, redirect, session, abort
import sys
from app import app, db
from .forms import LoginForm, RegisterForm, EventDetailForm
from .models import User, Event


@app.route('/<int:userid>')
def index(userid=None):
    if 'userid' in session:
        if session['userid'] == userid:
            events = User(userid).get_friends_events()
            return render_template('index.html', user=userid, event_list=events)
    return redirect('/login')


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        userid = User().authenticate(form.email.data, form.password.data)
        if userid is not None:
            session['userid'] = userid
            return redirect('/%s' % userid)
        else:
            return redirect('/login')

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        userid = User().create(form.email.data, form.password.data, form.username.data)
        if userid is not None:
            session['userid'] = userid
            return redirect('/%s' % userid)
        return "User exist! <br><a href = '/signup'></b>" + \
               "click here to sign up again</b></a>"

    return render_template('signup.html', form=form)


@app.route('/profile/<id>')
def profile(id):
    return render_template('profile.html', name=id)


@app.route('/event_detail/<int:eventid>')
def event_detail(eventid):
    event = Event(eventid).find()
    if event is None:
        return abort(404)
    return '{{event.name}}'
    #return render_template('event_detail.html', event)


@app.route('/create_event')
def create_event():
    form = EventDetailForm()
    if form.validate_on_submit():
        start_time = form.start_date.data + form.start_time.data
        end_time = form.start_date.data + form.end_time.data
        eventid = Event().create(session['userid'], form.name.data, form.description.data, form.location.data,
                                 start_time, end_time)
        if eventid is not None:
            return redirect('/%s' % session['userid'])
        return redirect('/create_event')

    return render_template('create_event.html')

