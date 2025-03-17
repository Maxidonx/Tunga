from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf.file import FileAllowed


# Post Form
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=250)])
    content = TextAreaField('Content', validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Post')

    def validate_title(self, field):
        if len(field.data) < 5:
            raise ValidationError('Title must be at least 5 characters long.')