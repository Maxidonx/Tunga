# filepath: /home/john-maxwell/Tunga-Assignments/Tunga/app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from flask_wtf.file import FileAllowed
from flask_login import current_user

# Registration Form
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, field):
        from app.models import User  # Import inside the method to avoid circular import
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This email is already registered. Please log in.')

# Profile Update Form
class ProfileUpdateForm(FlaskForm):
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d')
    profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    submit = SubmitField('Update Profile')

    @property
    def current_user(self):
        return current_user

# Login Form (Now uses Email instead of Username)
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])  # New: Login with Email
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Post Form
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=250)])
    content = TextAreaField('Content', validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Post')

    def validate_title(self, field):
        if len(field.data) < 5:
            raise ValidationError('Title must be at least 5 characters long.')