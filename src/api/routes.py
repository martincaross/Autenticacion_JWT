"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, TokenBlockedList
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager, create_access_token, get_jwt
from flask_bcrypt import Bcrypt


api = Blueprint('api', __name__)
app = Flask(__name__)
bcrypt = Bcrypt()

# Allow CORS requests to this API
CORS(api)

# @api.record
# def init_bcrypt(setup_state):
#     bcrypt.init_app(setup_state.app)

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

# Get users
@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

# Singup
@api.route('/signup', methods=['POST'])
def signup():
    body = request.get_json()
    email = body.get('email')
    fullname = body.get("fullname")
    password = body.get('password')

    if not email or not password:
        return jsonify({"msg": "Email and password required"}), 400
    
    if not fullname:
        return jsonify({"msg": "fullname es requerido"}), 400
    
    # Verificar si ya existe un usuario con ese email
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "User already exists"}), 409
    
    # Crear nuevo usuario
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, fullname=fullname, password=hashed_password, is_active=True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "msg": "User created successfully",
        "user": new_user.serialize()  # <--- Aquí usamos el serialize
    }), 201

# Login
@api.route('/login', methods=['POST'])
def login_user():
    body=request.get_json()
    user=User.query.filter_by(email=body["email"]).first()
    if user is None:
        return jsonify({"msg":"Correo no encontrado"}), 401
    is_valid_password=bcrypt.check_password_hash(user.password, body["password"])
    if not is_valid_password:
        return jsonify({"msg":"Clave inválida"}), 401
    payload = {
        "admin": False,
        "permissions":123123
    }
    # Generar el token
    token=create_access_token(identity=str(user.id), additional_claims=payload)
    return jsonify({"token":token}), 200


@api.route('/userinfo', methods=['GET'])
@jwt_required()
def user_info():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    payload = get_jwt()
    return jsonify({
        "user": user.serialize(),
        "payload": payload
    }), 200


@api.route('/private', methods=['GET'])
@jwt_required()
def private_route():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@api.route('/logout', methods=['POST'])
@jwt_required()
def user_logout():
    # se obtiene el payload del token
    payload = get_jwt()
    # se creo un registro del token bloqueado con el jti del token
    token_blocked = TokenBlockedList(jti=payload["jti"])
    # se guarda en la base de datos
    db.session.add(token_blocked)
    db.session.commit()
    return jsonify({"msg":"User logged out"})