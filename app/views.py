from flask import render_template, request, redirect, session, abort
from app import app
from .forms import LoginForm, RegisterForm, EventDetailForm
from .models import User, Event


@app.route('/home')
def index():
    if 'userid' in session:
        userid = session['userid']
        events = User(userid).get_friends_events()
        creator_name_list = {}
        for e in events:
            creator_id = e[6]
            creator = User(creator_id).find()
            if creator is None:
                abort(501)
            creator_name_list[creator_id] = creator[3]
        return render_template('index.html', user=userid, event_list=events, creators=creator_name_list)
    return redirect('/login')


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        userid = User().authenticate(form.email.data, form.password.data)
        if userid is not None:
            session['userid'] = userid
            return redirect('/home')
        else:
            return redirect('/login')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    if 'userid' in session:
        session.pop('userid', None)
        return redirect('/login')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        userid = User().create(form.email.data, form.password.data, form.username.data)
        if userid is not None:
            session['userid'] = userid
            return redirect('/home')
        return redirect('/signup')

    return render_template('signup.html', form=form)


@app.route('/profile/<int:userid>')
def profile(userid):
    return render_template('profile.html', name=userid)


@app.route('/event_detail/<int:eventid>')
def event_detail(eventid):
    event = Event(eventid).find()
    if event is None:
        return abort(404)
    return render_template('event_detail.html', event=event)


@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    form = EventDetailForm()
    if form.validate_on_submit():
        start_time = form.start_date.data + form.start_time.data
        end_time = form.start_date.data + form.end_time.data
        eventid = Event().create(session['userid'], form.name.data, form.description.data, form.location.data,
                                 start_time, end_time)
        if eventid is not None:
            return redirect('/home')
        return redirect('/create_event')

    return render_template('create_event.html', form=form)

