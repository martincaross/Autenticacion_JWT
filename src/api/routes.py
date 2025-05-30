"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)
bcrypt = Bcrypt()  # Aquí creamos la instancia

@api.record
def init_bcrypt(setup_state):
    bcrypt.init_app(setup_state.app)

@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/signup', methods=['POST'])
def signup():
    body = request.get_json()
    email = body.get('email')
    password = body.get('password')

    if not email or not password:
        return jsonify({"msg": "Email and password required"}), 400
    
    # Verificar si ya existe un usuario con ese email
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "User already exists"}), 409
    
    # Crear nuevo usuario
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=password, is_active=True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "msg": "User created successfully",
        "user": new_user.serialize()  # <--- Aquí usamos el serialize
    }), 201


@api.route('/login', methods=['POST'])
def login_user():
    body=request.get_json()
    user=User.query.filter_by(email=body["email"]).first()
    if user is None:
        return jsonify({"msg":"Correo no encontrado"}), 401
    is_valid_password=bcrypt.check_password_hash(user.password, body["password"])
    if not is_valid_password:
        return jsonify({"msg":"Clave inválida"}), 401
    # Generar el token
    token=create_access_token(identify=user.id)
    return jsonify({"token":token}), 200

@api.route('/private', methods=['GET'])
@jwt_required()
def private_route():
    current_user = get_jwt_identity()
    return jsonify({"msg": f"Bienvenido, {current_user}"}), 200
