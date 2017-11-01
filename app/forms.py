from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(message='Length should be between 4 and 15'
                                                                                   ' characters', min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=32)])


'''yyyy-mm-dd hh:mm'''
class EventDetailForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(), Length(message='Length should be between 1 and 64'
                                                                           ' characters', min=1, max=64)])
    start_date = StringField('start_date', validators=[InputRequired(), Length(message='Format: yyyymmdd',
                                                                               min=8, max=8)])
    start_time = StringField('start_time', validators=[InputRequired(), Length(message='Format: hhmm', min=4, max=4)])
    end_date = StringField('end_date', validators=[InputRequired(), Length(message='Length should be between 1 and 64'
                                                                           ' characters', min=1, max=64)])
    end_time = StringField('end_time', validators=[InputRequired(), Length(message='Format: hhmm', min=4, max=4)])
    location = StringField('location', validators=[InputRequired(), Length(max=255)])
    description = StringField('description', validators=[InputRequired(), Length(max=65535)])
