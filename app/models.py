from app import db,bcrypt
from flask_login import UserMixin
import re

tags=db.Table(
    'tags',
    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id')),
    db.Column('article_id',db.Integer,db.ForeignKey('article.id')))

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
    article_id=db.Column(db.Integer,db.ForeignKey('article.id'))

class Article(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    time=db.Column(db.DateTime)
    title=db.Column(db.String(48))
    body=db.Column(db.String(1024))
    comments=db.relationship('Comment',backref='article',lazy='dynamic')
    tags=db.relationship('Tag',
        secondary=tags,
        backref=db.backref('articles'),
        lazy='dynamic')
    def body_to_html(self,page='blog'):
        html=self.body
        #linebreak
        html=re.sub(r'\n',r'<br>',html)
        #image
        pattern=re.compile(r'\*img\*(.*?)\*img\*')
        if page=='blog':
            html=pattern.sub(r'<img class="img-fluid" src="static/upload/\1" alt="\1">',html)
        elif page=='article':
            html=pattern.sub(r'<img class="img-fluid" src="../static/upload/\1" alt="\1">',html)
        #bold
        pattern=re.compile(r'\*b\*(.*?)\*b\*')
        html=pattern.sub(r'<strong>\1</strong>',html)
        #italic
        pattern=re.compile(r'\*i\*(.*?)\*i\*')
        html=pattern.sub(r'<em>\1</em>',html)
        #underline
        pattern=re.compile(r'\*u\*(.*?)\*u\*')
        html=pattern.sub(r'<u>\1</u>',html)
        return html

class Tag(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(24))

class Album(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    time=db.Column(db.DateTime)
    title=db.Column(db.String(48))
    body=db.Column(db.String(1024))
    images=db.relationship('Image',backref='album',lazy='dynamic')

class Image(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    filename=db.Column(db.String(48))
    album_id=db.Column(db.Integer,db.ForeignKey('album.id'))
