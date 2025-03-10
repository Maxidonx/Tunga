from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import app, db, User, Post, bcrypt
from forms import RegisterForm, LoginForm, PostForm


with app.app_context():
    db.create_all()

@app.route('/')
def index():
    posts = Post.query.all()
    print("All Posts Retrieved:", posts)  # Debugging
    return render_template('index.html', posts=posts)

# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username already exists. Please choose a different one.", "danger")
            return redirect(url_for('register'))
        
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully! You can now log in.", "success")
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password", "danger")
    return render_template('login.html', form=form)

# LOGOUT
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

# CREATE A POST
@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    
    if form.validate_on_submit():
        print("Form validated")  # Debugging

        if current_user.is_authenticated:
            print("Current User ID:", current_user.id)  # Debugging

            new_post = Post(
                title=form.title.data,
                content=form.content.data,
                user_id=current_user.id,
            )
            db.session.add(new_post)
            db.session.flush()  # Debugging: Helps detect errors before commit
            print("Flushed Post ID:", new_post.id)  # Debugging
            db.session.commit()
            
            print("New Post Created:", new_post.id, new_post.title, new_post.content)  # Debugging
            
            flash("Post created successfully!", "success")
            return redirect(url_for('index'))
        else:
            flash("You must be logged in to create a post.", "danger")

    return render_template('create_post.html', form=form)

# UPDATE A POST
@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash("You are not authorized to edit this post.", "danger")
        return redirect(url_for('index'))

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post updated successfully!", "success")
        return redirect(url_for('index'))

    # Pre-fill form with post data
    form.title.data = post.title
    form.content.data = post.content
    return render_template('edit_post.html', form=form)

# DELETE A POST
@app.route('/posts/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for('index'))
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
