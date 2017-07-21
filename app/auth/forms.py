from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from ..models import User
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(6,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me login')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators = [Required(), Length(6,64),Email()])
    username = StringField('username', validators = [Required(), Length(1-32),Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Usernames must have only letters,''numbers,dots or underscores')])
    password = PasswordField('Password',  validators=[Required(), EqualTo('password2', message='two passwords must match!')])
    password2= PasswordField('confirm Password', validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('username already registered')
