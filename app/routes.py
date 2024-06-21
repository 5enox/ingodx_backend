import json
from .models import db, User, Order
from flask_restx import Namespace, Resource, fields
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

authorizations = {
    "JWT": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
    }
}
api = Namespace('api', description='Resource API',
                authorizations=authorizations)


user_model = api.model('User', {
    'user_id': fields.Integer(readOnly=True),
    'username': fields.String(required=True, description='The user name'),
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password'),
    'full_name': fields.String(required=True, description='The user full name'),
    'user_type': fields.String(required=True, description='The type of user (customer or delivery)')
})

order_model = api.model('Order', {
    'item_description': fields.String(required=True, description='Description of the item'),
    'pickup_address': fields.String(required=True, description='Pickup address'),
    'delivery_address': fields.String(required=True, description='Delivery address'),
})

login_model = api.model('Login', {
    'username': fields.String(required=True, description='Username of the user'),
    'password': fields.String(required=True, description='Password of the user'),
})


@api.route('/users')
class UserAPI(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        return User.query.all()


@api.route('/register')
class Register(Resource):
    @api.expect(user_model, validate=True)
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        full_name = data.get('full_name')
        user_type = data.get('user_type')

        password_hash = generate_password_hash(password)

        # Uncomment the following lines if you want to add the user to the database
        new_user = User(
            username=username,
            password_hash=password_hash,
            email=email,
            full_name=full_name,
            user_type=user_type
        )
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully!"}, 201


@api.route('/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            # Password matches, generate JWT token
            access_token = create_access_token(identity=user.user_id)
            return {'message': 'Login successful!', 'access_token': access_token}, 200
        else:
            return {"message": "Invalid username or password"}, 401


# Example protected endpoint (requires authentication)
@api.route('/orders')
class OrderAPI(Resource):
    @api.doc(security='JWT')
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        return Order.query.filter_by(user_id=current_user_id).all()

    @api.expect(order_model, validate=True)
    @api.doc(security='JWT')
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        data = request.json
        user_id = data.get('user_id')
        item_description = data.get('item_description')
        pickup_address = data.get('pickup_address')
        delivery_address = data.get('delivery_address')

        new_order = Order(
            user_id=current_user_id,
            item_description=item_description,
            pickup_address=pickup_address,
            delivery_address=delivery_address
        )
        db.session.add(new_order)
        db.session.commit()

        return {"message": "Order created successfully!"}, 201


@api.route('/order/<int:order_id>')
class OrderDetail(Resource):
    @api.doc(security='JWT')
    @jwt_required()
    def get(self, order_id):
        current_user_id = get_jwt_identity()
        order = Order.query.filter_by(
            order_id=order_id, user_id=current_user_id).first()
        if order:
            return order
        else:
            return {"message": "Order not found"}, 404

    @api.doc(security='JWT')
    @jwt_required()
    def post(self, order_id):
        current_user_id = get_jwt_identity()
        order = Order.query.filter_by(
            order_id=order_id, user_id=current_user_id).first()
        if order:
            data = request.json
            item_description = data.get('item_description')
            pickup_address = data.get('pickup_address')
            delivery_address = data.get('delivery_address')

            order.item_description = item_description
            order.pickup_address = pickup_address
            order.delivery_address = delivery_address

            db.session.commit()
            return {"message": "Order updated successfully!"}, 200
        else:
            return {"message": "Order not found"}, 404

    @api.doc(security='JWT')
    @jwt_required()
    def delete(self, order_id):
        current_user_id = get_jwt_identity()
        order = Order.query.filter_by(
            order_id=order_id, user_id=current_user_id).first()
        if order:
            db.session.delete(order)
            db.session.commit()
            return {"message": "Order deleted successfully!"}, 200
        else:
            return {"message": "Order not found"}, 404


@api.route('/delivery/orders')
class DeliveryOrders(Resource):
    @api.doc(security='JWT')
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        if User.query.filter_by(user_id=current_user_id, user_type='delivery').first():
            return Order.query.all()
        else:
            return {"message": "Access denied"}, 403

    @api.doc(security='JWT')
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        if User.query.filter_by(user_id=current_user_id, user_type='delivery').first():
            data = request.json
            order_id = data.get('order_id')
            order = Order.query.filter_by(
                order_id=order_id).first()
            if order:
                if order.status == 'pending':
                    order.status = 'accepted'
                    db.session.commit()
                    return {"message": "Order accepted successfully!"}, 200
                else:
                    return {"message": "Order has already been accepted or delivered"}, 400
            else:
                return {"message": "Order not found"}, 404
        else:
            return {"message": "Access denied"}, 403
