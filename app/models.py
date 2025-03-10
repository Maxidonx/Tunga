from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "default_secret")  # Secure secret key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Define Base Class for SQLAlchemy
class Base(DeclarativeBase):
    pass

# Initialize Extensions
db = SQLAlchemy(model_class=Base)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)  # Enable migrations

db.init_app(app)  # Ensure database initialization

# User Model
class User(db.Model, UserMixin):
    id = db.mapped_column(db.Integer, primary_key=True)
    username = db.mapped_column(db.String(50), unique=True, nullable=False)
    password = db.mapped_column(db.String(100), nullable=False)
    posts = db.relationship('Post', back_populates='author', cascade="all, delete-orphan")

# Blog Post Model
class Post(db.Model):
    id = db.mapped_column(db.Integer, primary_key=True)
    title = db.mapped_column(db.String(250), nullable=False)
    content = db.mapped_column(db.Text, nullable=False)
    user_id = db.mapped_column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    author = db.relationship('User', back_populates='posts')

# Flask-Login User Loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create Database Tables
with app.app_context():
    db.create_all()
