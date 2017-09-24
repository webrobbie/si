from . import app
from app import db,bcrypt
from flask_login import UserMixin
import re

post_tag_table=db.Table(
    'tags',
    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id')),
    db.Column('post_id',db.Integer,db.ForeignKey('post.id')))

class Sisi(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(48))
    password=db.Column(db.String(96))
    def set_password(self,password):
        self.password=bcrypt.generate_password_hash(password).decode('utf-8')
    def check_password(self,password):
        if bcrypt.check_password_hash(self.password,password):
            return True

class Comment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    time=db.Column(db.DateTime)
    author=db.Column(db.String(48))
    body=db.Column(db.String(1024))
    post_id=db.Column(db.Integer,db.ForeignKey('post.id'))
    image_id=db.Column(db.Integer,db.ForeignKey('image.id'))
    parent_id=db.Column(db.Integer,db.ForeignKey('comment.id'))
    children=db.relationship('Comment',backref=db.backref('parent',remote_side=[id]),lazy='dynamic')

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    time=db.Column(db.DateTime)
    title=db.Column(db.String(48))
    body=db.Column(db.String(1024))
    comments=db.relationship('Comment',backref='post',lazy='dynamic')
    album=db.Column(db.Boolean)
    images=db.relationship('Image',backref='post',lazy='dynamic')
    tags=db.relationship('Tag',
        secondary=post_tag_table,
        backref=db.backref('posts'),
        lazy='dynamic')
    def body_to_html(self,location):#{{{
        html=self.body
        #linebreak
        if location in ('article','album'):
            html=re.sub(r'\n',r'<br>',html)
        else:
            html=re.sub(r'\n',r'',html)
        #image
        pattern=re.compile(r'\*img\*(.*?)\*img\*')
        if location in ('article','album'):
            html=pattern.sub(r'<img class="center-img" src="../static/upload/\1" alt="\1">',html)
        else:
            html=pattern.sub(r'<img class="center-img" src="static/upload/\1" alt="\1">',html)
        if location in ('article','album'):
            #bold
            pattern=re.compile(r'\*b\*(.*?)\*b\*')
            html=pattern.sub(r'<strong>\1</strong>',html)
            #italic
            pattern=re.compile(r'\*i\*(.*?)\*i\*')
            html=pattern.sub(r'<em>\1</em>',html)
            #underline
            pattern=re.compile(r'\*u\*(.*?)\*u\*')
            html=pattern.sub(r'<u>\1</u>',html)
        else:
            pattern=re.compile(r'\*[biu]\*')
            html=pattern.sub(r'',html)
        return html
    #}}}

class Image(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    filename=db.Column(db.String(48))
    body=db.Column(db.String(1024))
    post_id=db.Column(db.Integer,db.ForeignKey('post.id'))
    rank=db.Column(db.Integer)
    comments=db.relationship('Comment',backref='image',lazy='dynamic')
    def body_to_html(self):#{{{
        html=self.body
        #linebreak
        html=re.sub(r'\n',r'<br>',html)
        #bold
        pattern=re.compile(r'\*b\*(.*?)\*b\*')
        html=pattern.sub(r'<strong>\1</strong>',html)
        #italic
        pattern=re.compile(r'\*i\*(.*?)\*i\*')
        html=pattern.sub(r'<em>\1</em>',html)
        #underline
        pattern=re.compile(r'\*u\*(.*?)\*u\*')
        html=pattern.sub(r'<u>\1</u>',html)

class Tag(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(24))
