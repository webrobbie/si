from flask_wtf import Form
from wtforms import StringField,TextAreaField,FileField,SelectMultipleField,widgets,PasswordField
from wtforms.validators import DataRequired

class ArticleForm(Form):
    title=StringField('Title',validators=[
        DataRequired(message='Input required')])
    body=TextAreaField('Body',validators=[
        DataRequired(message='Input required')])
    file=FileField('File',validators=[])

class AlbumForm(Form):
    title=StringField('Title',validators=[
        DataRequired(message='Input required')])
    body=TextAreaField('Body',validators=[])
    file=FileField('File',validators=[
        DataRequired(message='Input required')])

class LoginForm(Form):
    password=PasswordField('Password',validators=[
        DataRequired(message='Input required')])

class CommentForm(Form):
    author=StringField('Author',validators=[
        DataRequired(message='Input required')])
    body=TextAreaField('Body',validators=[
        DataRequired(message='Input required')])

class ImageForm(Form):
    body=TextAreaField('Body',validators=[])
    file=FileField('File',validators=[])
