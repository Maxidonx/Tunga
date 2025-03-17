from app import app, db
from app.post.forms import PostForm
from app.post.models import Post
from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os



post_blueprint = Blueprint('post', __name__, template_folder='templates')


@post_blueprint.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post/post_detail.html', post=post)

@post_blueprint.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        image_file = None
        if form.image.data:
            image_file = secure_filename(form.image.data.filename)
            image_path = os.path.join(app.root_path, 'static/post_images', image_file)
            form.image.data.save(image_path)
        post = Post(title=form.title.data, content=form.content.data, image_file=image_file, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Form validation failed. Please check your input.', 'danger')
    return render_template('post/create_post.html', form=form)

@post_blueprint.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('You are not authorized to edit this post.', 'danger')
        return redirect(url_for('index'))
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        if form.image.data:
            image_file = secure_filename(form.image.data.filename)
            image_path = os.path.join(app.root_path, 'static/post_images', image_file)
            form.image.data.save(image_path)
            post.image_file = image_file
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('post.post_detail', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('post/edit_post.html', form=form, post=post)

@post_blueprint.route('/post/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('You are not authorized to delete this post.', 'danger')
        return redirect(url_for('index'))
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('index'))