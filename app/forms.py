from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,FileField,SelectMultipleField,widgets,PasswordField
from wtforms.validators import DataRequired

class NewPostForm(FlaskForm):
    title=StringField('title',validators=[
        DataRequired(message='Input required')])
    body=TextAreaField('body',validators=[
        DataRequired(message='Input required')])
    file=FileField('file',validators=[])

class NewAlbumForm(FlaskForm):
    title=StringField('title',validators=[
        DataRequired(message='Input required')])
    body=TextAreaField('body',validators=[])
    file=FileField('file',validators=[
        DataRequired(message='Input required')])

class LoginForm(FlaskForm):
    password=PasswordField('password',validators=[
        DataRequired(message='Input required')])
