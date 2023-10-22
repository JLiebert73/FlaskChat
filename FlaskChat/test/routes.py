from flask import render_template, flash, redirect, url_for
from test import app, db, bcrypt
from test.forms import RegistrationForm, LoginForm, AccountUpdateForm, ContentForm, FindForm
from test.models import User, Post
from flask_login import login_user, current_user, logout_user
from test import url_stack, socketio
from datetime import datetime
from sqlalchemy import or_
import secrets
import os
from test.models import ChatMessage
from flask import request, jsonify
from flask_socketio import SocketIO, emit


@app.route("/")
def home():
    posts=Post.query.all()
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user1 = User(username=form.username.data, email=form.email.data, password=pw)
        db.session.add(user1)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user1 = User.query.filter_by(email=form.email.data).first()
        if user1 and bcrypt.check_password_hash(user1.password, form.password.data):
            login_user(user1, remember=form.remember.data)
            if len(url_stack):
                url = url_stack.pop()
                url_stack.clear()
                return redirect(url)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please try again.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('login'))


def save(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/Images', picture_name)
    form_picture.save(picture_path)
    return picture_name


@app.route("/account")
def account():
    if current_user.is_authenticated:
        posts=Post.query.filter_by(author=current_user).all()
        imagefile = url_for('static', filename='Images/' + current_user.image_file)
        return render_template('account.html', posts=posts, title='Account', image_file=imagefile)
    else:
        url_stack.append(url_for('account'))
        flash(f'You are not logged in.', 'danger')
        return redirect(url_for('login'))


@app.route("/update", methods=['GET', 'POST'])
def update():
    form = AccountUpdateForm()
    if current_user.is_authenticated:
        user = current_user
        if form.validate_on_submit():
            # Update user details
            user.username = form.username.data
            user.email = form.email.data
            if form.password.data:
                user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            if form.profile_picture.data:
                image = save(form.profile_picture.data)
                user.image_file = image
            db.session.commit()

            # Update associated posts
            posts = Post.query.filter_by(user_id=user.id).all()
            for post in posts:
                post.author = user
            db.session.commit()

            flash(f'Your account details have been updated!', 'success')
            return redirect(url_for('account'))
        return render_template('update.html', title='Update', form=form)
    flash(f'You have to log in first.', 'danger')
    url_stack.append(url_for('update'))
    return redirect(url_for('login'))


@app.route('/write', methods=['GET', 'POST'])
def write():
    form = ContentForm()
    if not current_user.is_authenticated:
        flash(f'You have to login first!', 'danger')
        url_stack.append(url_for('write'))
        return redirect(url_for('login'))
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash(f'Your write-up has been posted!', 'success')
        return redirect(url_for('home'))
    return render_template('write.html', title='Write Something!', form=form)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    search_option = request.args.get('search_option')
    if search_option == 'username':
        users = User.query.filter_by(username=query).all()
        if users is None:
            flash(f'No such user exists', 'danger')
            return redirect(url_for('search'))
        for user in users:
            posts=Post.query.filter_by(author=user).all()
            imagefile = url_for('static', filename='Images/' + user.image_file)
            return render_template('other_account.html', user=user, posts=posts, title=user.username+"'s Account", image_file=imagefile)
        flash(f'No such user exists', 'danger')
        return redirect(url_for('search'))
    
    elif search_option == 'title':
        posts = Post.query.filter_by(title=query).all()
        if posts:
            return view_post(posts)
        else:
            flash(f'No such post exists', 'danger')
            return redirect(url_for('search'))
    return render_template('search.html')


def view_post(posts):
    return render_template('view_post.html', posts=posts)


@app.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post.author != current_user:
        flash('Only the author can delete this post.', 'danger')
        return render_template('view_post.html', post=post)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully.', 'success')
    return redirect(url_for('home'))


@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get(post_id)
    if post.author != current_user:
        flash('Only the author can edit this post.', 'danger')
        return render_template('view_post.html', post=post)
    form=ContentForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash(f'Post updated successfully!', 'success')
        return redirect(url_for('home'))
    form.title.data=post.title
    form.content.data=post.content
    return render_template('write.html', title='Edit Post', form=form, Legend='Edit Post')

@app.route('/user/<int:post_id>')
def user(post_id):
    post = Post.query.get(post_id)
    user=post.author
    posts=Post.query.filter_by(author=user).all()
    imagefile = url_for('static', filename='Images/' + user.image_file)
    return render_template('other_account.html', user=user, posts=posts, title=user.username+"'s Account", image_file=imagefile)

@app.route('/user_list')
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)

@app.route('/chat')
def chat():
    return redirect('/user_list')

@socketio.on('message')
def handle_message(message):
    emit('message', message, broadcast=True)

@app.route('/receive')
def receive():
    return render_template('receive.html')

@app.route('/chat_individual')
def chat_individual():
    return render_template('chat.html')

