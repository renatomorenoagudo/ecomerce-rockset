#importação
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin 


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)
CORS(app)

# Modelagem
#user (id, username, passworld)
class User(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key=True)
   username = db.column (db.String(80), unique=True)
#unique nao deixa cadastrar nomes iguais
   password =db.Column (db.String(80), nullable=True)