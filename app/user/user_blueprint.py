from app import app, db, bcrypt
from app.user.forms import ProfileUpdateForm
from app.post.models import Post
from app.auth.models import User
from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import logging

# Initialize the user blueprint
user_blueprint = Blueprint('user', __name__, template_folder='templates')

# Set up logging for the user blueprint
user_logger = logging.getLogger('user')
user_logger.setLevel(logging.ERROR)
handler = logging.FileHandler('user.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
user_logger.addHandler(handler)

# Global error handler for the user blueprint
@user_blueprint.errorhandler(Exception)
def handle_user_exception(e):
    user_logger.error(f"Unhandled Exception in user_blueprint: {str(e)}", exc_info=True)
    flash("An error occurred. Please try again later.", "danger")
    return redirect(url_for('user.profile'))

@user_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    try:
        form = ProfileUpdateForm()
        if form.validate_on_submit():
            # Handle profile picture upload
            if form.profile_picture.data:
                filename = secure_filename(form.profile_picture.data.filename)
                file_path = os.path.join('static/profile_picture', filename)
                form.profile_picture.data.save(file_path)
                current_user.profile_picture = filename

            # Update other details
            if form.first_name.data:
                current_user.first_name = form.first_name.data
            if form.last_name.data:
                current_user.last_name = form.last_name.data
            if form.date_of_birth.data:
                current_user.date_of_birth = form.date_of_birth.data

            db.session.commit()
            flash("Profile updated successfully!", "success")
            return redirect(url_for('user.profile'))
        return render_template('user/profile.html', form=form)
    except Exception as e:
        user_logger.error(f"Error in profile route: {str(e)}", exc_info=True)
        flash("An error occurred while updating your profile. Please try again later.", "danger")
        return redirect(url_for('user.profile'))