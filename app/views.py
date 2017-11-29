from flask import render_template, request, redirect, session, abort
from app import app
from .forms import LoginForm, RegisterForm, EventDetailForm
from .models import User, Event
import os


@app.route('/home')
def home():
    if 'userid' in session:
        userid = session['userid']
        events = User(userid).get_following_events()
        creator_name_list = {}
        for e in events:
            creator_id = e[6]
            if creator_id not in creator_name_list:
                creator = User(creator_id).find()
                if creator is None:
                    return abort(501)
                creator_name_list[creator_id] = creator[1]
        return render_template('home.html', user=userid, event_list=events, creators=creator_name_list)
    return redirect('/login')


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'userid' in session:
        return redirect('/home')
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
    if 'userid' not in session:
        return redirect('/login')
    user = User(userid).find()
    if user is None:
        return abort(404)
    events_created = User(userid).get_events_created()
    events_participated = User(userid).get_events_participated()
    creator_name_list = {}
    for e in events_participated:
        creator_id = e[6]
        if creator_id not in creator_name_list:
            creator = User(creator_id).find()
            if creator is None:
                abort(501)
            creator_name_list[creator_id] = creator[1]

    return render_template('profile.html', current_user=session['userid'], user_profile=user,
                           event_created=events_created, events_participated=events_participated,
                           creators=creator_name_list, user=userid)


@app.route('/register/<int:eventid>')
def register(eventid):
    if 'userid' not in session:
        return redirect('/login')
    userid = session['userid']
    if User(userid).register(eventid) is True:
        return redirect('/profile/%d' % userid)
    return redirect('/home')


@app.route('/event_detail/<int:eventid>')
def event_detail(eventid):
    if 'userid' not in session:
        return redirect('/login')
    event = Event(eventid).find()
    if event is None:
        return abort(404)
    if User(session['userid']).check_register(event[0]) is True:
        registered = True
    else:
        registered = False
    participants = Event(eventid).get_participants()
    return render_template('event_detail.html', event=event, user=session['userid'], participants=participants, registered=registered)


@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if 'userid' not in session:
        return redirect('/login')
    form = EventDetailForm()
    userid = session['userid']

    if form.validate_on_submit():
        start_time = form.start_date.data
        end_time = form.end_date.data
        eventid = Event().create(session['userid'], form.name.data, form.description.data, form.location.data,
                                 start_time, end_time)
        if eventid is not None:
            return redirect('/home')
        file = request.files['file']
        if file:
            fname = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(fname)
            os.rename(fname, os.path.join(app.config['UPLOAD_FOLDER'], eventid + '.jpg'))
        return redirect('/create_event')

    return render_template('create_event.html', form=form, user=userid)


@app.route('/add_friend', methods=['GET', 'POST'])
def add_friend():
    userid = session['userid']
    userinfo = request.form['userinfo']
    userlist = User().search_user(userinfo)
    userlist = list(userlist)
    for i in range(len(userlist)):
        if User(userid).check_follow(userlist[i][0]) is True:
            userlist[i] += (1,)
        userlist[i] += (0,)
    return render_template('add_friend.html', userlist=userlist, user=userid)


@app.route('/add/<string:userid>')
def add(userid):
    if 'userid' not in session:
        return redirect('/login')
    if User(session['userid']).follow(userid) is False:
        return 'Cannot follow'
    return redirect('/show_friends/%s' % session['userid'])


@app.route('/show_friends/<int:userid>')
def show_friends(userid):
    followers = User(userid).get_followers()
    followings = User(userid).get_followings()
    return render_template('show_friends.html', followers=followers, followings=followings, user=userid)


@app.route('/change_profile')
def change_profile():
    userid = session['userid']
    return render_template('change_profile.html', user=userid)

