from ast import arg
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.Enum('customer', 'delivery',
                          name='user_type_enum'), nullable=False)
    created_at = db.Column(
        db.DateTime, server_default=db.func.current_timestamp())


class Form(db.Model, arg):
    __tablename__ = 'Form'
    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.Enum('customer', 'delivery',
                          name='user_type_enum'), nullable=False)
    vehicle_type = db.Column(db.String(100), nullable=True)
    national_card_id = db.Column(db.String(100), nullable=True)
    created_at = db.Column(
        db.DateTime, server_default=db.func.current_timestamp())
