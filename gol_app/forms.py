from wtforms import StringField, validators, PasswordField, EmailField, TextAreaField, BooleanField, SubmitField, ValidationError
import flask_wtf
from gol_app.models import User


class SignUp(flask_wtf.FlaskForm):

    username = StringField('Username', validators=[validators.DataRequired(),
                                                   validators.Length(min=5, max=32)])
    password = PasswordField('Password', validators=[validators.DataRequired(),
                                                     validators.Length(min=5)])
    password_again = PasswordField('Repeat password', validators=[validators.DataRequired(),
                                                                  validators.Length(min=5)])
    email = EmailField('Email (optional)', validators=[validators.Optional()])
    about = TextAreaField('About me (optional)', validators=[validators.Optional()])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        if User.query.all():
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username already exists. Choose another one.')

    def validate_email(self, email):
        if User.query.all():
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email already exists. Choose another one.')


class LogIn(flask_wtf.FlaskForm):

    username = StringField('Username', validators=[validators.DataRequired(),
                                                           validators.Length(min=5, max=32)])
    password = PasswordField('Password', validators=[validators.DataRequired(),
                                                             validators.Length(min=5)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')
