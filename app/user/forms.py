# filepath: /home/john-maxwell/Tunga-Assignments/Tunga/app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, DateField
from flask_wtf.file import FileAllowed
from flask_login import current_user



# # Profile Update Form
class ProfileUpdateForm(FlaskForm):
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d')
    profile_picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    submit = SubmitField('Update Profile')

    @property
    def current_user(self):
        return current_user