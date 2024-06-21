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


class Order(db.Model):
    __tablename__ = 'Orders'
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'Users.user_id'), nullable=False)
    item_description = db.Column(db.Text, nullable=False)
    pickup_address = db.Column(db.Text, nullable=False)
    delivery_address = db.Column(db.Text, nullable=False)
    order_status = db.Column(db.Enum('pending', 'in_progress', 'completed',
                             'cancelled', name='order_status_enum'), default='pending')
    created_at = db.Column(
        db.DateTime, server_default=db.func.current_timestamp())


class Delivery(db.Model):
    __tablename__ = 'Deliveries'
    delivery_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'Orders.order_id'), nullable=False)
    delivery_user_id = db.Column(
        db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    delivery_status = db.Column(db.Enum('accepted', 'in_progress', 'delivered',
                                'failed', name='delivery_status_enum'), default='accepted')
    delivery_fee = db.Column(db.Numeric(10, 2), nullable=False)
    delivery_date = db.Column(db.DateTime)


class Payment(db.Model):
    __tablename__ = 'Payments'
    payment_id = db.Column(db.Integer, primary_key=True)
    delivery_id = db.Column(db.Integer, db.ForeignKey(
        'Deliveries.delivery_id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(
        db.DateTime, server_default=db.func.current_timestamp())
    payment_status = db.Column(db.Enum(
        'pending', 'completed', 'failed', name='payment_status_enum'), default='pending')
