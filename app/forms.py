from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class MovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    description = TextAreaField('Movie Description', validators=[DataRequired()])
    poster = FileField('Movie Poster', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
