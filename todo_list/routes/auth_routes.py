from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models.models_user import User


class AuthRoutes:
    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.auth_bp = Blueprint('auth_bp', __name__)
        self.register_routes()
        self.app.register_blueprint(self.auth_bp)

    def register_routes(self):
        self.auth_bp.route('/login', methods=['POST'])(self.login)
        self.auth_bp.route('/register', methods=['POST'])(self.register)

    def login(self):
        data = request.get_json()
        # print Payload in console
        print("Login payload:", data)

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"msg": "Username and password are required."}), 400

        user = User.find_by_username(username, db=self.db)
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"msg": "Invalid username or password."}), 401

        access_token = create_access_token(identity=user.username)
        return jsonify(access_token=access_token), 200

    def register(self):
        data = request.get_json()
        # print Payload in console
        print("Register payload:", data)

        username = data.get('username', '').strip()
        password = data.get('password', '')
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()

        errors = []
        if not username or not password:
            errors.append("Username and password are required.")
        if not email:
            errors.append("Email is required.")
        if not phone:
            errors.append("Phone number is required.")
        if errors:
            return jsonify({"errors": errors}), 400

        if User.find_by_username(username, db=self.db):
            return jsonify({"msg": "Username already exists."}), 400

        hashed_password = generate_password_hash(password)
        user = User(username=username, password_hash=hashed_password, email=email, phone=phone, db=self.db)
        user.save()

        return jsonify({"msg": "User registered successfully.", "user_id": user.id}), 201
