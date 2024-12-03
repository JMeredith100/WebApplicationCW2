from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField


# This is the form used for logging in
class LoginForm(FlaskForm):
    username = StringField('username')
    password = StringField('password')

# This is the form used for registering to the platform
class RegisterForm(FlaskForm):
    username = StringField('username')
    password = StringField('password')
    dob = DateField('dob')

# This is the form used for creating posts
class PostForm(FlaskForm):
    title = StringField('post title')
    content = TextAreaField('content')