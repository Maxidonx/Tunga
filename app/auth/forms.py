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
        from app.auth.models import User  # Import inside the method to avoid circular import
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This email is already registered. Please log in.')

# Login Form (Now uses Email instead of Username)
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])  # New: Login with Email
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')