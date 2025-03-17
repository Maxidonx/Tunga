from app import db, bcrypt
from app.auth.forms import RegisterForm, LoginForm
from app.auth.models import User
from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_user, login_required, logout_user, current_user



auth_blueprint = Blueprint('auth', __name__, template_folder='templates')



@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()
        
        if existing_user:
            flash("Username already exists. Please choose a different one.", "danger")
            return redirect(url_for('auth.register'))
        if existing_email:
            flash("Email already registered. Please log in.", "danger")
            return redirect(url_for('auth.login'))
         
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        
        flash("Account created successfully! You can now log in.", "success")
        return redirect(url_for('auth.login'))
     
    return render_template('auth/register.html', form=form)

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid email or password", "danger")
    return render_template('auth/login.html', form=form)

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))
