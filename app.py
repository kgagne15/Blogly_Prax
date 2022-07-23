"""Blogly application."""

from crypt import methods
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()

@app.route('/')
def list_users(): 
    """Show list of all users in db"""
    return redirect('/users')

@app.route('/users')
def show_users():
    """Show users and link to detail page for user"""
    users = User.query.all()
    return render_template('list_users.html', users=users)

@app.route('/users/<int:user_id>')
def details_page(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).all()
    return render_template('details.html', user=user, posts=posts)

@app.route('/users/new')
def add_user_form():
    return render_template('user_form.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit_form.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    edited_user = User.query.get(user_id)
    edited_user.first_name = request.form['first_name']
    edited_user.last_name = request.form['last_name']
    edited_user.image_url = request.form['image_url']

    db.session.add(edited_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect('/users')

@app.route('/posts/<int:post_id>')
def show_posts(post_id):
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    user_first = post.user.first_name
    user_last = post.user.last_name
    return render_template('posts.html', post=post, first=user_first, last=user_last, tags=tags)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def submit_edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['updated-title']
    post.content = request.form['updated-content']
    tags = request.form.getlist('tag')

    for item in post.tagged_items:
        db.session.delete(item)
        db.session.commit()

    
    db.session.add(post)
    db.session.commit()

    for t in tags:
        if t not in post.tags: 
            new_post_tag = PostTag(post_id=post.id, tag_id=t)
            db.session.add(new_post_tag)
            db.session.commit()
    return redirect(f'/posts/{post_id}')

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('new_post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post_submit(user_id):
    post_title = request.form['new-title']
    post_content = request.form['new-content']
    tags = request.form.getlist('tag')
    new_post = Post(title=post_title, content=post_content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    for t in tags:
        new_post_tag = PostTag(post_id=new_post.id, tag_id=t)
        db.session.add(new_post_tag)
        db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    for item in post.tagged_items:
        db.session.delete(item)
        db.session.commit()
    db.session.delete(post)
    db.session.commit()
    return redirect('/users')

@app.route('/tags')
def list_all_tags():
    tags = Tag.query.all()
    return render_template('list_tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template('tag_details.html', tag=tag, posts=posts)

@app.route('/tags/new')
def add_tag():
    return render_template('add_tag.html')

@app.route('/tags/new', methods=["POST"])
def add_tag_submit():
    tag_name = request.form['new-tag']
    new_tag = Tag(name=tag_name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect ('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag_submit(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    name = request.form['new-tag-name']
    tag.name = name
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')