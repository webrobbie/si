from app import db,bcrypt
from flask_login import UserMixin

tags=db.Table(
    'tags',
    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id')),
    db.Column('post_id',db.Integer,db.ForeignKey('post.id')))

class Sisi(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String)
    password=db.Column(db.String)
    def set_password(self,password):
        self.password=bcrypt.generate_password_hash(password).decode('utf-8')
    def check_password(self,password):
        if bcrypt.check_password_hash(self.password,password):
            return True

class Comment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    time=db.Column(db.DateTime)
    title=db.Column(db.String)
    body=db.Column(db.String)
    post_id=db.Column(db.Integer,db.ForeignKey('post.id'))

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    time=db.Column(db.DateTime)
    title=db.Column(db.String)
    body=db.Column(db.String)
    comments=db.relationship('Comment',backref='post',lazy='dynamic')
    tags=db.relationship('Tag',
        secondary=tags,
        backref=db.backref('posts'),
        lazy='dynamic')

class Tag(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)

class Album(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    time=db.Column(db.DateTime)
    title=db.Column(db.String)
    body=db.Column(db.String)
    images=db.relationship('Image',backref='album',lazy='dynamic')

class Image(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    filename=db.Column(db.String)
    album_id=db.Column(db.Integer,db.ForeignKey('album.id'))
