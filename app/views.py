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
# admin.add_view(ModelView(Article,db.session))
# admin.add_view(ModelView(Album,db.session))
# admin.add_view(ModelView(Tag,db.session))
# admin.add_view(ModelView(Comment,db.session))
#}}}
#BLOG{{{
@app.route('/',methods=['GET','POST'])
def blog():
    articles=Article.query.all()
    articles.sort(key=operator.attrgetter('time'))
    tags=Tag.query.all()
    if request.method=='POST':
        kw=request.form['keyword']
        filter_tags=[]
        for tag_id in request.form.getlist('tag_id'):
            filter_tags.append(Tag.query.get(tag_id))
        ordered_articles=[]
        for article in articles:
            score=len(set(article.tags).intersection(filter_tags))
            if not filter_tags:
                score=1
#special form for year, month, day, before, after...
                ordered_articles.append((score,article))
        ordered_articles.sort(reverse=True)
        articles=[article[1] for article in ordered_articles]
    return render_template('blog.html',articles=articles,tags=tags)
#}}}
#NEW POST{{{
@app.route('/new_article',methods=['GET','POST'])
@login_required
def new_article():
    form=NewArticleForm()
    if form.validate_on_submit():
        files=[f for f in request.files.getlist('file') if f.filename]
        for f in files:
            if f.filename in form.body.data:
                f.save(app.config['UPLOAD_TO']+f.filename)
        p=Article(
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
        return redirect(url_for('blog'))
    tags=Tag.query.all()
    return render_template('new_article.html',form=form,tags=tags)
#}}}
#ARTICLE PAGE{{{
@app.route('/article/<article_id>')
def article(article_id):
    article=Article.query.get(article_id)
    return render_template('article.html',article=article)
#}}}
#EDIT POST{{{
@app.route('/edit_article/<article_id>',methods=['GET','POST'])
@login_required
def edit_article(article_id):
    form=NewArticleForm()
    article=Article.query.get(article_id)
    if request.method=='POST':
        article.title=form.title.data
        article.body=form.body.data
        article.tags=[Tag.query.get(tag_id) for tag_id in request.form.getlist('tag_id')]
        for new_tag in request.form.getlist('new_tags'):
            if new_tag:
                t=Tag(name=new_tag)
                db.session.add(t)
                article.tags.append(t)
        db.session.commit()
        return redirect(url_for('blog'))
        
    tags=Tag.query.all()
    article_tags=article.tags.all()
    form.body.data=article.body#pre-populate textarea in template not working
    return render_template('edit_article.html',
        article=article,
        form=form,
        tags=tags,
        article_tags=article_tags)
#}}}
#DELETE POST{{{
@app.route('/delete_article/<article_id>')
@login_required
def delete_article(article_id):
    p=Article.query.get(article_id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('blog'))
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
    return redirect(url_for('blog'))
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
            return redirect(url_for('blog'))
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
    return redirect(url_for('blog'))
#}}}
#TEST{{{
@app.route('/test')
def test():
    return 'test'
#}}}
