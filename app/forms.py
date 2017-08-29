from flask_wtf import Form
from wtforms import StringField,TextAreaField,FileField,SelectMultipleField,widgets,PasswordField
from wtforms.validators import DataRequired

class NewArticleForm(Form):
    title=StringField('title',validators=[
        DataRequired(message='Input required')])
    body=TextAreaField('body',validators=[
        DataRequired(message='Input required')])
    file=FileField('file',validators=[])

class NewAlbumForm(Form):
    title=StringField('title',validators=[
        DataRequired(message='Input required')])
    body=TextAreaField('body',validators=[])
    file=FileField('file',validators=[
        DataRequired(message='Input required')])

class LoginForm(Form):
    password=PasswordField('password',validators=[
        DataRequired(message='Input required')])
