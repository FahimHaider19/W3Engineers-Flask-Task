from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch
from flask_jwt_extended import JWTManager
from flask_restx import Api
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://user-name:strong-password@localhost:5432/testdb"
app.config['JWT_SECRET_KEY'] = secrets.token_hex(16)
app.config['JWT_HEADER_TYPE'] = ''
db = SQLAlchemy(app)
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
jwt = JWTManager(app)
api = Api(app)

from routes import auth, snf
api.add_namespace(auth)
api.add_namespace(snf)

if __name__ == '__main__':
    app.run(debug=True)
