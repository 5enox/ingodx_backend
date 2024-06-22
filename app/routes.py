import json
from .models import db, User, Form
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
    'username': fields.String(required=True, description='The user name'),
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password'),
    'full_name': fields.String(required=True, description='The user full name'),
    'user_type': fields.String(required=True, description='The type of user (customer or delivery)')
})


login_model = api.model('Login', {
    'username': fields.String(required=True, description='Username of the user'),
    'password': fields.String(required=True, description='Password of the user'),
})

form_model = api.model('UserForm', {
    'full_name': fields.String(required=True, description='The user full name'),
    'user_type': fields.String(required=True, description='The type of user (customer or delivery)'),
    'vehicle_type': fields.String(required=False, description='The type of vehicle the delivery person uses'),
    'national_card_id': fields.String(required=False, description='The national card ID of the delivery person'),

})


@ api.route('/register')
class Register(Resource):
    @ api.expect(user_model, validate=True)
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


@ api.route('/login')
class Login(Resource):
    @ api.expect(login_model, validate=True)
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


@api.route('/user_form')
class UserForm(Resource):
    @api.expect(form_model, validate=True)
    @api.doc(security='JWT')
    @jwt_required()
    def post(self):
        data = request.json
        full_name = data.get('full_name')
        user_type = data.get('user_type')
        vehicle_type = data.get('vehicle_type')
        national_card_id = data.get('national_card_id')
        current_user_id = get_jwt_identity()

        form_data = Form(
            user_id=current_user_id,
            full_name=full_name,
            user_type=user_type,
            vehicle_type=vehicle_type,
            national_card_id=national_card_id
        )
        db.session.add(form_data)
        db.session.commit()

        return {"message": "Form data stored successfully!"}, 200


@api.route('/user_data')
class UserData(Resource):
    @api.doc(security='JWT')
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if user:
            return {
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'user_type': user.user_type
            }, 200
        else:
            return {"message": "User not found"}, 404
