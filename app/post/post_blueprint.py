from app import app, db
from app.post.forms import PostForm
from app.post.models import Post
from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import logging

# Initialize the post blueprint
post_blueprint = Blueprint('post', __name__, template_folder='templates')

# Set up logging for the post blueprint
post_logger = logging.getLogger('post')
post_logger.setLevel(logging.ERROR)
handler = logging.FileHandler('post.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
post_logger.addHandler(handler)

# Global error handler for the post blueprint
@post_blueprint.errorhandler(Exception)
def handle_post_exception(e):
    post_logger.error(f"Unhandled Exception in post_blueprint: {str(e)}", exc_info=True)
    flash("An error occurred. Please try again later.", "danger")
    return redirect(url_for('index'))

@post_blueprint.route('/post/<int:post_id>')
def post_detail(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        return render_template('post/post_detail.html', post=post)
    except Exception as e:
        post_logger.error(f"Error in post_detail route: {str(e)}", exc_info=True)
        flash("An error occurred while fetching the post. Please try again later.", "danger")
        return redirect(url_for('index'))

@post_blueprint.route('/post/new', methods=['GET', 'POST'])
@login_required
def create_post():
    try:
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
    except Exception as e:
        post_logger.error(f"Error in create_post route: {str(e)}", exc_info=True)
        flash("An error occurred while creating the post. Please try again later.", "danger")
        return redirect(url_for('index'))

@post_blueprint.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    try:
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
    except Exception as e:
        post_logger.error(f"Error in edit_post route: {str(e)}", exc_info=True)
        flash("An error occurred while editing the post. Please try again later.", "danger")
        return redirect(url_for('index'))

@post_blueprint.route('/post/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        if post.author != current_user:
            flash('You are not authorized to delete this post.', 'danger')
            return redirect(url_for('index'))
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        post_logger.error(f"Error in delete_post route: {str(e)}", exc_info=True)
        flash("An error occurred while deleting the post. Please try again later.", "danger")
        return redirect(url_for('index'))