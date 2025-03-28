from app import app
from app.post.models import Post
from app.auth.models import User
from flask import render_template, request

from app import login_manager
from app.auth.auth_blueprint import auth_blueprint
from app.post.post_blueprint import post_blueprint
from app.user.user_blueprint import user_blueprint
from app.api.api_blueprint import  api_blueprint



app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(post_blueprint, url_prefix='/post')
app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(api_blueprint, url_prefix='/api') 


@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=True)