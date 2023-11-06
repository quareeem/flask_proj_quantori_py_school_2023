from flask import render_template, request, redirect, flash, session, url_for
from sqlalchemy import select
from app_blogc import bcrypt, app, db
from app_blogc.models import Favorite, Group, User, Post, association_table
from app_blogc.routes_auth import token_required
from app_blogc.utils import get_categories



@app.route('/')
@token_required(False)
def home(current_user=None):
    categories = get_categories(current_user)
    posts = Post.query.all()
    return render_template('index.html', posts=posts, user=current_user, categories=categories)


@app.route('/post/<int:post_id>')
@token_required(True)
def view_post(current_user, post_id):
    post = Post.query.get_or_404(post_id)
    is_author = current_user.id == post.user_id

    is_favorite = Favorite.query.filter_by(user_id=current_user.id, post_id=post_id).first() is not None

    return render_template('posts_detail.html', post=post, is_author=is_author, is_favorite=is_favorite)



@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@token_required(True)
def edit_post(current_user, post_id):
    post = Post.query.get_or_404(post_id)
    
    if current_user.id != post.user_id:
        flash('You can only edit your own posts.', 'danger')
        return redirect(url_for('view_post', post_id=post_id))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        post.title = title
        post.content = content
        db.session.commit()
        
        flash('Your post has been updated!', 'success')
        return redirect(url_for('view_post', post_id=post_id))
    
    return render_template('edit_post.html', post=post)


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@token_required(True)
def delete_post(current_user, post_id):
    post = Post.query.get_or_404(post_id)
    
    if current_user.id != post.user_id:
        flash('You can only delete your own posts.', 'danger')
        return redirect(url_for('view_post', post_id=post_id))
    
    db.session.delete(post)
    db.session.commit()
    
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))



@app.route('/post/<int:post_id>/favorite', methods=['POST'])
@token_required(True)
def favorite_post(current_user, post_id):
    if request.method == 'POST':
        # Check if already favorited to avoid duplicates
        favorite = Favorite.query.filter_by(user_id=current_user.id, post_id=post_id).first()
        if not favorite:
            new_favorite = Favorite(user_id=current_user.id, post_id=post_id)
            db.session.add(new_favorite)
            db.session.commit()
            flash('The post has been added to your favorites!', 'success')
        else:
            flash('This post is already in your favorites.', 'info')
        return redirect(url_for('view_post', post_id=post_id))


@app.route('/group/<int:group_id>')
@token_required(False)
def group_feed(current_user, group_id):
    categories = get_categories(current_user)
    posts = None
    if current_user:
        posts = Post.query.filter(Post.group_id == group_id).all()

    return render_template('posts_groups.html', posts=posts, user=current_user, categories=categories)


@app.route('/my_posts')
@token_required(True)  # Set to True because this route should require a user to be logged in
def my_posts(current_user):
    categories = get_categories(current_user)
    posts = Post.query.filter_by(author=current_user).all()

    return render_template('posts_my.html', posts=posts, user=current_user, categories=categories)


@app.route('/my_favs')
@token_required(True)  # Set to True because this route should require a user to be logged in
def my_favs(current_user):
    categories = get_categories(current_user)
    posts = Post.query.join(Favorite, Post.id == Favorite.post_id).filter(Favorite.user_id == current_user.id).all()

    return render_template('posts_favs.html', posts=posts, user=current_user, categories=categories)


@app.route('/create', methods=['GET', 'POST'])
@token_required(True)
def create_post(current_user):
    if request.method == 'GET':
        groups = None
        if current_user:
            groups = current_user.groups
        return render_template('create_post.html', user=current_user, groups=groups)


    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        group_id = request.form.get('groupSelect')
        group = Group.query.get(group_id)



        new_post = Post(title=title, content=content, user_id=current_user.id, group_id=group.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Post was successful', 'success')
        return redirect(url_for('home'))


@app.route('/about')
@token_required(False)
def about(current_user=None):
    return render_template('about.html', user=current_user,)