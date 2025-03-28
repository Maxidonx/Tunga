import logging
from logging.handlers import RotatingFileHandler
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse
from app import db, bcrypt
from app.auth.models import User
from app.post.models import Post
import jwt
import datetime
from functools import wraps
from app.config import Config
from flask import Flask


app=Flask(__name__)
# Create API Blueprint
api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint)
log_file = "app.log"
handler = RotatingFileHandler(log_file, maxBytes=100000, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

app.logger.setLevel(logging.ERROR)
# JWT Secret Key
SECRET_KEY = Config.SECRET_KEY


@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Unhandled Exception: {str(e)}", exc_info=True)
    return jsonify({'message': 'An error occurred while processing your request'}), 500


# Middleware to check JWT tokens
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token or " " not in token:
            app.logger.warning('Token format is invalid!')
            return jsonify({'message': 'Token format is invalid!'}), 401

        try:
            token = token.split(" ")[1]  # Remove 'Bearer' from token
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.get(data["id"])
            if not current_user:
                app.logger.warning('User not found for the token!')
                return jsonify({'message': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            app.logger.warning('Token has expired!')
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            app.logger.warning('Invalid token!')
            return jsonify({'message': 'Invalid token!'}), 401
        except Exception as e:
            app.logger.error(f'Error decoding token: {str(e)}', exc_info=True)
            return jsonify({'message': f'Error: {str(e)}'}), 500

        return f(*args, current_user=current_user, **kwargs)
    return decorated

# User Registration API
class Register(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username cannot be blank')
        parser.add_argument('email', type=str, required=True, help='Email cannot be blank')
        parser.add_argument('password', type=str, required=True, help='Password cannot be blank')

        args = parser.parse_args()

        if User.query.filter_by(username=args['username']).first():
            app.logger.info(f"Registration failed: Username '{args['username']}' already taken")
            return {'message': 'Username already taken'}, 400
        if User.query.filter_by(email=args['email']).first():
            app.logger.info(f"Registration failed: Email '{args['email']}' already registered")
            return {'message': 'Email already registered'}, 400

        hashed_pw = bcrypt.generate_password_hash(args['password']).decode('utf-8')
        user = User(username=args['username'], email=args['email'], password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        app.logger.info(f"User '{args['username']}' registered successfully")
        return {'message': 'User registered successfully'}, 201

# User Login API
class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data.get("email")).first()
        if user and bcrypt.check_password_hash(user.password, data.get("password")):
            token = jwt.encode(
                {'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
                SECRET_KEY,
                algorithm="HS256"
            )
            app.logger.info(f"User '{user.email}' logged in successfully")
            return {'token': token}, 200
        app.logger.warning(f"Login failed for email: {data.get('email')}")
        return {'message': 'Invalid credentials'}, 401


# Get User Profile (Protected)
class Profile(Resource):
    @token_required
    def get(self, current_user):
        return {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "profile_picture": current_user.profile_picture
        }

    @token_required
    def put(self, current_user):
        data = request.get_json()
        current_user.username = data.get("username", current_user.username)
        current_user.email = data.get("email", current_user.email)
        current_user.first_name = data.get("first_name", current_user.first_name)
        current_user.last_name = data.get("last_name", current_user.last_name)
        current_user.profile_picture = data.get("profile_picture", current_user.profile_picture)

        date_of_birth = data.get("date_of_birth")
        if date_of_birth:
            try:
                current_user.date_of_birth = datetime.datetime.strptime(date_of_birth, "%Y-%m-%d")
            except ValueError:
                return {'message': 'Invalid date format. Use YYYY-MM-DD'}, 400

        db.session.commit()
        return {'message': 'Profile updated successfully'}, 200

# Get All Posts
class PostList(Resource):
    def get(self):
        posts = Post.query.all()
        return [{"id": post.id, "title": post.title, "content": post.content, "author": post.author.username} for post in posts], 200

# Get, Update, Delete Post (Protected)
class PostDetail(Resource):
    @token_required
    def get(self, current_user, post_id):
        post = Post.query.get_or_404(post_id)
        return {"id": post.id, "title": post.title, "content": post.content, "author": post.author.username}, 200

    @token_required
    def put(self, current_user, post_id):
        post = Post.query.get_or_404(post_id)
        if post.author != current_user:
            return {'message': 'Unauthorized to edit this post'}, 403
        
        data = request.get_json()
        post.title = data.get("title", post.title)
        post.content = data.get("content", post.content)
        db.session.add(post)
        db.session.commit()
        return {'message': 'Post updated successfully'}, 200

    @token_required
    def delete(self, current_user, post_id):
        post = Post.query.get_or_404(post_id)
        if post.author != current_user:
            app.logger.warning(f"Unauthorized delete attempt by user '{current_user.username}' on post ID {post_id}")
            return {'message': 'Unauthorized to delete this post'}, 403

        db.session.delete(post)
        db.session.commit()
        app.logger.info(f"Post ID {post_id} deleted by user '{current_user.username}'")
        return {'message': 'Post deleted successfully'}, 200

# Register API Routes
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Profile, '/profile')
api.add_resource(PostList, '/posts')
api.add_resource(PostDetail, '/post/<int:post_id>')
