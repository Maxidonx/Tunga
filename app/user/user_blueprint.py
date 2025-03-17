from app import app, db, bcrypt
from app.user.forms import ProfileUpdateForm
from app.post.models import Post
from app.auth.models import User
from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import  login_required, current_user
from werkzeug.utils import secure_filename

import os

user_blueprint = Blueprint('user', __name__, template_folder='templates')

@user_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
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