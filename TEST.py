from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy


# class CustomFlask(Flask):
#     jinja_options = Flask.jinja_options.copy()
#     jinja_options.update(dict(
#       block_start_string='{%',
#       block_end_string='%}',
#       variable_start_string='((',
#       variable_end_string='))',
#       comment_start_string='{#',
#       comment_end_string='#}',
#     ))


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
Bootstrap(app)
db = SQLAlchemy(app)
# app.jinja_env.variable_start_string = '{{ '
# app.jinja_env.variable_end_string = ' }}'


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

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

if __name__ == '__main__':
    app.run(debug=True)
