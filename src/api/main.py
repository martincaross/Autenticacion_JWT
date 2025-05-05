from flask import Flask
from flask_cors import CORS
from api.routes import api
from api.models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdb.db'  # o la URI que uses
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app, supports_credentials=True)  # <- aquí es importante habilitarlo para todo el backend

app.register_blueprint(api, url_prefix='/api')
