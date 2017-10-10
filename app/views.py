from flask import render_template,redirect,url_for,flash,request,session
from flask_login import login_user,logout_user,login_required,current_user
from datetime import datetime
import PIL.Image
import re,os,operator
from . import app,db
from .forms import *
from .models import *
from .utils import *

#ARTICLES{{{
@app.route('/',methods=['GET','POST'])
def articles():
    posts=Post.query.filter(Post.album==False).order_by(Post.time.desc()).all()
    return render_template('articles.html',posts=posts)
#}}}
#ARTICLE{{{
@app.route('/article/<post_id>',methods=['GET','POST'])
def article(post_id):
    form=CommentForm()
    post=Post.query.get(post_id)
    if form.validate_on_submit():
        if form.author.data in ('si','Si') and not current_user.is_authenticated:
            flash('Enter another name.','red')
            return redirect(url_for('article',post_id=post_id))
        c=Comment(
            author=form.author.data,
            body=form.body.data,
            post=post,
            time=datetime.now())
        db.session.add(c)
        post.comments.append(c)
        db.session.commit()
        flash('Comment added.','green')
        return redirect(url_for('article',post_id=post_id))
    return render_template('article.html',form=form,post=post)
#}}}
#NEW ARTICLE{{{
@app.route('/new_article/',methods=['GET','POST'])
@login_required
def new_article():
    form=ArticleForm()
    if form.validate_on_submit():
        for f in request.files.getlist('file'):
            name=os.path.splitext(f.filename)[0]
            if f.filename and name+'.jpg' in form.body.data:#always f.filename?
                if f.filename not in os.listdir(app.config['UPLOAD_TO']):
                    # name=os.path.splitext(f.filename)[0]
                    big_pic=PIL.Image.open(f)
                    big_pic.thumbnail((800,2000))
                    big_pic.save(app.config['UPLOAD_TO']+name+'.jpg')
                    small_pic=PIL.Image.open(f)
                    small_pic.thumbnail((240,240))
                    small_pic.save(app.config['UPLOAD_TO']+name+'_thumbnail.jpg')
                else:
                    flash(f.filename+' not saved (filename already existing)','red')
        post=Post(
            title=form.title.data,
            body=form.body.data,
            time=datetime.now(),
            album=False)
        db.session.add(post)
        for tag_id in request.form.getlist('tag_id'):
            post.tags.append(Tag.query.get(tag_id))
        for new_tag in request.form.getlist('new_tags'):
            if new_tag:
                existing_tag=Tag.query.filter_by(name=new_tag).first()
                if not existing_tag:
                    t=Tag(name=new_tag)
                    db.session.add(t)
                    post.tags.append(t)
                else:
                    post.tags.append(existing_tag)
        db.session.commit()
        flash('Article created.','green')
        return redirect(url_for('article',post_id=post.id))
    tags=Tag.query.all()
    return render_template('new_article.html',form=form,tags=tags)
#}}}
#EDIT ARTICLE{{{
@app.route('/edit_article/<post_id>',methods=['GET','POST'])
@login_required
def edit_article(post_id):
    form=ArticleForm()
    post=Post.query.get(post_id)
    if form.validate_on_submit():
        for f in request.files.getlist('file'):
            if f.filename and f.filename in form.body.data:
                if f.filename not in os.listdir(app.config['UPLOAD_TO']):
                    name=os.path.splitext(f.filename)[0]
                    big_pic=PIL.Image.open(f)
                    big_pic.thumbnail((800,2000))
                    big_pic.save(app.config['UPLOAD_TO']+name+'.jpg')
                    small_pic=PIL.Image.open(f)
                    small_pic.thumbnail((240,240))
                    small_pic.save(app.config['UPLOAD_TO']+name+'_thumbnail.jpg')
                else:
                    flash(f.filename+' not saved (filename already existing).','red')
        post.title=form.title.data
        post.body=form.body.data
        post.tags=[Tag.query.get(tag_id) for tag_id in request.form.getlist('tag_id')]
        for new_tag in request.form.getlist('new_tags'):
            if new_tag:
                existing_tag=Tag.query.filter_by(name=new_tag).first()
                if not existing_tag:
                    t=Tag(name=new_tag)
                    db.session.add(t)
                    post.tags.append(t)
                else:
                    post.tags.append(existing_tag)
        db.session.commit()
        flash('Changes have been saved.','green')
        return redirect(url_for('article',post_id=post_id))
    tags=Tag.query.all()
    post_tags=post.tags.all()
    form.body.data=post.body
    form.title.data=post.title
    return render_template('edit_article.html',
        post=post,
        form=form,
        tags=tags)
#}}}
#DELETE ARTICLE{{{
@app.route('/delete_article/<post_id>')
@login_required
def delete_article(post_id):
    post=Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Article deleted.','green')
    return redirect(url_for('articles'))
#}}}

#ALBUMS{{{
@app.route('/albums')
def albums():
    posts=Post.query.filter(Post.album==True).order_by(Post.time.desc()).all()
    return render_template('albums.html',posts=posts)
#}}}
#ALBUM{{{
@app.route('/album/<post_id>',methods=['GET','POST'])
def album(post_id):
    form=CommentForm()
    post=Post.query.get(post_id)
    if form.validate_on_submit():
        if form.author.data in ('si','Si') and not current_user.is_authenticated:
            flash('Enter another name.','red')
            return redirect(url_for('album',post_id=post_id))
        c=Comment(
            author=form.author.data,
            body=form.body.data,
            post=post,
            time=datetime.now())
        db.session.add(c)
        post.comments.append(c)
        db.session.commit()
        flash('Comment added.','green')
        return redirect(url_for('album',post_id=post_id))
    return render_template('album.html',form=form,post=post)
#}}}
#NEW ALBUM{{{
@app.route('/new_album',methods=['GET','POST'])
@login_required
def new_album():
    form=AlbumForm()
    if form.validate_on_submit():
        post=Post(
            title=form.title.data,
            body=form.body.data,
            time=datetime.now(),
            album=True)
        db.session.add(post)
        files=[f for f in request.files.getlist('file') if f.filename]
        for f in files:
            name=''
            if f.filename not in os.listdir(app.config['UPLOAD_TO']):
                # f.save(app.config['UPLOAD_TO']+f.filename)
                name=os.path.splitext(f.filename)[0]
                big_pic=PIL.Image.open(f)
                big_pic.thumbnail((800,2000))
                big_pic.save(app.config['UPLOAD_TO']+name+'.jpg')
                small_pic=PIL.Image.open(f)
                small_pic.thumbnail((240,240))
                small_pic.save(app.config['UPLOAD_TO']+name+'_thumbnail.jpg')
            else:
                flash(f.filename+' not saved (filename already existing).','red')
            # image=Image(filename=f.filename,post=post)
            image=Image(filename=name+'.jpg',post=post)
            db.session.add(image)
        images=post.images.all()
        for image,n in zip(images,range(1,len(images)+1)):
            image.rank=n
        for tag_id in request.form.getlist('tag_id'):
            post.tags.append(Tag.query.get(tag_id))
        for new_tag in request.form.getlist('new_tags'):
            if new_tag:
                existing_tag=Tag.query.filter_by(name=new_tag).first()
                if not existing_tag:
                    t=Tag(name=new_tag)
                    db.session.add(t)
                    post.tags.append(t)
                else:
                    post.tags.append(existing_tag)
        db.session.commit()
        flash('Album created.','green')
        return redirect(url_for('album',post_id=post.id))
    tags=Tag.query.all()
    return render_template('new_album.html',form=form,tags=tags)
#}}}
#EDIT ALBUM{{{
@app.route('/edit_album/<post_id>',methods=['GET','POST'])
@login_required
def edit_album(post_id):
    form=AlbumForm()
    post=Post.query.get(post_id)
    if form.validate_on_submit():
        files=[f for f in request.files.getlist('file') if f.filename]
        for f in files:
            name=''
            if f.filename not in os.listdir(app.config['UPLOAD_TO']):
                # f.save(app.config['UPLOAD_TO']+f.filename)
                name=os.path.splitext(f.filename)[0]
                big_pic=PIL.Image.open(f)
                big_pic.thumbnail((800,2000))
                big_pic.save(app.config['UPLOAD_TO']+name+'.jpg')
                small_pic=PIL.Image.open(f)
                small_pic.thumbnail((240,240))
                small_pic.save(app.config['UPLOAD_TO']+name+'_thumbnail.jpg')
            else:
                flash(f.filename+' not saved (filename already existing).','red')
            image=Image(filename=name+'.jpg',post=post)
            db.session.add(image)
        images=post.images.all()
        for image,n in zip(images,range(1,len(images)+1)):
            image.rank=n
        post.title=form.title.data
        post.body=form.body.data
        post.tags=[Tag.query.get(tag_id) for tag_id in request.form.getlist('tag_id')]
        for new_tag in request.form.getlist('new_tags'):
            if new_tag:
                existing_tag=Tag.query.filter_by(name=new_tag).first()
                if not existing_tag:
                    t=Tag(name=new_tag)
                    db.session.add(t)
                    post.tags.append(t)
                else:
                    post.tags.append(existing_tag)
        db.session.commit()
        flash('Changes have been saved.','green')
        return redirect(url_for('album',post_id=post_id))
    tags=Tag.query.all()
    post_tags=post.tags.all()
    form.body.data=post.body
    form.title.data=post.title
    return render_template('edit_album.html',
        post=post,
        form=form,
        tags=tags)
#}}}
#DELETE ALBUM{{{
@app.route('/delete_album/<post_id>')
@login_required
def delete_album(post_id):
    p=Post.query.get(post_id)
    for img in p.images.all():
        db.session.delete(img)
    db.session.delete(p)
    db.session.commit()
    flash('Album deleted.','green')
    return redirect(url_for('albums'))
#}}}

#IMAGE{{{
@app.route('/image/<img_id>',methods=['GET','POST'])
def image(img_id):
    image=Image.query.get(img_id)
    form=CommentForm()
    if form.validate_on_submit():
        if form.author.data in ('si','Si') and not current_user.is_authenticated:
            flash('Enter another name.','red')
            return redirect(url_for('image',img_id=img_id))
        c=Comment(
            author=form.author.data,
            body=form.body.data,
            image=image,
            time=datetime.now())
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('image',img_id=img_id))
    return render_template('image.html',
        image=image,
        Image=Image,
        form=form)
#}}}
#EDIT IMAGE{{{
@app.route('/edit_image/<img_id>',methods=['GET','POST'])
@login_required
def edit_image(img_id):
    form=ImageForm()
    image=Image.query.get(img_id)
    if form.validate_on_submit():
        for f in request.files.getlist('file'):
            if f.filename and f.filename not in os.listdir(app.config['UPLOAD_TO']):
                # f.save(app.config['UPLOAD_TO']+f.filename)
                name=os.path.splitext(f.filename)[0]
                big_pic=PIL.Image.open(f)
                big_pic.thumbnail((800,2000))
                big_pic.save(app.config['UPLOAD_TO']+name+'.jpg')
                small_pic=PIL.Image.open(f)
                small_pic.thumbnail((240,240))
                small_pic.save(app.config['UPLOAD_TO']+name+'_thumbnail.jpg')
                image.filename=name+'.jpg'
            else:
                flash(f.filename+' not saved (filename already existing).','red')
        image.body=form.body.data
        images=image.post.images.all()
        for image,n in zip(images,range(1,len(images)+1)):
            image.rank=n
        db.session.commit()
        flash('Changes have been saved.','green')
        return redirect(url_for('image',img_id=img_id))
    return render_template('edit_image.html',
        image=image,
        form=form)
#}}}
#DELETE IMAGE{{{
@app.route('/delete_image/<img_id>')
@login_required
def delete_image(img_id):
    image=Image.query.get(img_id)
    album=image.post
    db.session.delete(image)
    images=image.post.images.all()
    for image,n in zip(images,range(1,len(images)+1)):
        image.rank=n
    db.session.commit()
    return redirect(url_for('album',post_id=album.id))
    # p=Post.query.get(post_id)
    # db.session.delete(p)
    # db.session.commit()
    # flash('Album deleted.','green')
    # return redirect(url_for('albums'))
#}}}
#REPLY COMMENT{{{
@app.route('/reply_comment/<comment_id>',methods=['GET','POST'])
def reply_comment(comment_id):
    parent=Comment.query.get(comment_id)
    form=CommentForm()
    if form.validate_on_submit():
        c=Comment(
            author=form.author.data,
            body=form.body.data,
            # post=post,
            time=datetime.now(),
            parent=parent)
        db.session.add(c)
        # post.comments.append(c)
        db.session.commit()
        flash('Comment added.','green')
        if parent.image:
            return redirect(url_for('image',img_id=parent.image.id))
        elif parent.post.album:
            return redirect(url_for('album',post_id=parent.post.id))
        else:
            return redirect(url_for('article',post_id=parent.post.id))
    return render_template('reply_comment.html',form=form,parent=parent)
# }}}
#DELETE COMMENT{{{
@app.route('/delete_comment/<comment_id>')
@login_required
def delete_comment(comment_id):
    c=Comment.query.get(comment_id)
    post=image=None
    if c.post:
        post=c.post
    elif c.image:
        image.c.image
    db.session.delete(c)
    db.session.commit()
    flash('Comment deleted.','green')
    if image:
        return redirect(url_for('image',img_id=image.id))
    elif post:
        if post.album:
            return redirect(url_for('album',post_id=post.id))
        else:
            return redirect(url_for('article',post_id=post.id))
#}}}
#SEARCH (not working, or results){{{
@app.route('/search',methods=['GET','POST'])
def search():
    posts=Post.query.all()
    tags=Tag.query.all()
    if request.method=='POST':
        #get keyword
        kw=request.form['keyword']
        #get selected tags
        selected_tags=[]
        for tag_id in request.form.getlist('tag_id'):
            selected_tags.append(Tag.query.get(tag_id))
        #get tagged posts
        # selected_posts=[]
        posts_id=[]
        for post in posts:
            if set(selected_tags)==set(selected_tags).intersection(post.tags.all()):
                if kw in post.title+post.body:
                    posts_id.append(post.id)
        # selected.sort(key=operator.attrgetter('time'),reverse=True)
        # session['posts']=selected_posts
        # return str(session['posts'])
        posts_id.sort(reverse=True)
        session['posts_id']=posts_id
        return redirect(url_for('results'))
    return render_template('search.html',tags=tags)
#}}}
#RESULTS{{{
@app.route('/results')
def results():
    posts=[Post.query.get(post_id) for post_id in session['posts_id']]
    return render_template('results.html',posts=posts)
#}}}
#LOGIN{{{
@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        sisi=Sisi.query.first()
        if sisi.check_password(form.password.data):
            login_user(sisi)
            flash('Welcome, Sisi!','green')
            return redirect(url_for('articles'))
        flash('Wrong password...','red')
        return redirect(url_for('login'))
    return render_template('login.html',form=form)
#}}}
#LOGOUT{{{
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were just logged out.','green')
    return redirect(url_for('articles'))
#}}}
