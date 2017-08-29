from flask import render_template,redirect,url_for,flash,request
from flask_login import login_user,logout_user,login_required,current_user
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
import re,operator
from . import app,db,admin
from .forms import *
from .models import *
from .utils import *

#ADMIN{{{
@login_required
admin.add_view(ModelView(Post,db.session))
@login_required
admin.add_view(ModelView(Album,db.session))
@login_required
admin.add_view(ModelView(Tag,db.session))
@login_required
admin.add_view(ModelView(Comment,db.session))
#}}}
#INDEX{{{
@app.route('/',methods=['GET','POST'])
def index():
    posts=Post.query.all()
    posts.sort(key=operator.attrgetter('time'))
    tags=Tag.query.all()
    if request.method=='POST':
        kw=request.form['keyword']
        filter_tags=[]
        for tag_id in request.form.getlist('tag_id'):
            filter_tags.append(Tag.query.get(tag_id))
        ordered_posts=[]
        for post in posts:
            score=len(set(post.tags).intersection(filter_tags))
            if not filter_tags:
                score=1
#special form for year, month, day, before, after...
                ordered_posts.append((score,post))
        ordered_posts.sort(reverse=True)
        posts=[post[1] for post in ordered_posts]
    return render_template('index.html',posts=posts,tags=tags)
#}}}
#NEW POST{{{
@app.route('/new_post',methods=['GET','POST'])
@login_required
def new_post():
    form=NewPostForm()
    if form.validate_on_submit():
        files=[f for f in request.files.getlist('file') if f.filename]
        for f in files:
            if f.filename in form.body.data:
                f.save(app.config['UPLOAD_TO']+f.filename)
        p=Post(
            title=form.title.data,
            body=form.body.data,
            time=datetime.now())
        for tag_id in request.form.getlist('tag_id'):
            p.tags.append(Tag.query.get(tag_id))
        for new_tag in request.form.getlist('new_tags'):
            if new_tag:
                t=Tag(name=new_tag)
                db.session.add(t)
                p.tags.append(t)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('index'))
    tags=Tag.query.all()
    return render_template('new_post.html',form=form,tags=tags)
#}}}
#EDIT POST{{{
@app.route('/edit_post/<post_id>',methods=['GET','POST'])
@login_required
def edit_post(post_id):
    form=NewPostForm()
    post=Post.query.get(post_id)
    if request.method=='POST':
        post.title=form.title.data
        post.body=form.body.data
        post.tags=[Tag.query.get(tag_id) for tag_id in request.form.getlist('tag_id')]
        for new_tag in request.form.getlist('new_tags'):
            if new_tag:
                t=Tag(name=new_tag)
                db.session.add(t)
                p.tags.append(t)
        db.session.commit()
        return redirect(url_for('index'))
        
    tags=Tag.query.all()
    post_tags=post.tags.all()
    form.body.data=post.body#pre-populate textarea in template not working
    return render_template('edit_post.html',
        post=post,
        form=form,
        tags=tags,
        post_tags=post_tags)
#}}}
#DELETE POST{{{
@app.route('/delete_post/<post_id>')
@login_required
def delete_post(post_id):
    p=Post.query.get(post_id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('index'))
#}}}
#ALBUMS{{{
@app.route('/albums')
def albums():
    albums=Album.query.all()
    albums.sort(key=operator.attrgetter('time'))
    return render_template('albums.html',albums=albums)
#}}}
#NEW ALBUM{{{
@app.route('/new_album',methods=['GET','POST'])
@login_required
def new_album():
    form=NewAlbumForm()
    if form.validate_on_submit():
        album=Album(
            title=form.title.data,
            body=re.sub(r'\n','<br>',form.body.data),
            time=datetime.now())
        files=[f for f in request.files.getlist('file') if f.filename]
        for f in files:
            f.save(app.config['UPLOAD_TO']+f.filename)
            image=Image(filename=f.filename)
            image.album=album
            db.session.add(image)
        for tag_id in request.form.getlist('tag_id'):
            album.tags.append(Tag.query.get(tag_id))
        for new_tag in request.form.getlist('new_tags'):
            if new_tag:
                tag=Tag(name=new_tag)
                db.session.add(tag)
                album.tags.append(tag)
        db.session.add(album)
        db.session.commit()
        return redirect(url_for('albums'))
    tags=Tag.query.all()
    return render_template('new_album.html',form=form,tags=tags)
#}}}
#DELETE ALBUM{{{
@app.route('/delete_album/<album_id>')
@login_required
def delete_album(album_id):
    a=Album.query.get(album_id)
    db.session.delete(a)
    db.session.commit()
    return redirect(url_for('index'))
#}}}
#LOGIN{{{
@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        sisi=Sisi.query.first()
        if sisi.check_password(form.password.data):
            login_user(sisi)
            flash('Welcome, Sisi!','success')
            return redirect(url_for('index'))
        flash('Wrong password...','danger')
        return redirect(url_for('login'))
    return render_template('login.html',form=form)
#}}}
#LOGOUT{{{
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were just logged out.','info')
    return redirect(url_for('index'))
#}}}
#TEST{{{
@app.route('/test')
def test():
    return 'test'
#}}}
