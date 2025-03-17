# from datetime import datetime, timezone
# from app import db
# # from app.auth.models import User
# from flask_login import UserMixin

# # User Model
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)
#     first_name = db.Column(db.String(50), nullable=True)
#     last_name = db.Column(db.String(50), nullable=True)
#     nationality = db.Column(db.String(50), nullable=True)
#     date_of_birth = db.Column(db.Date, nullable=True)
#     profile_picture = db.Column(db.String(150), nullable=True, default='default.jpg')
#     posts = db.relationship('Post', back_populates='author', cascade="all, delete-orphan")