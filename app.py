#importação
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user


app = Flask(__name__)
app.config['SECRET_KEY']="minha_chave_123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)


# Modelagem: user (id, username, passworld)

class User(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key=True)
   username = db.column (db.String(80))
                         #,nullable=True, unique=True)
   password =db.Column (db.String(30), nullable=True)
#OBS:unique nao deixa cadastrar nomes iguais


# Product (id, name, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)


# AUTENTICAÇÃO:
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# LOGIN (user, password)
@app.route('/login', methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get("username")).first()

    if user and data.get("password") == user.password:
            login_user(user)
            return jsonify({"message":"Logged in successfully!"})
    return jsonify({"message":"Unauthorized. Invalid credentials"}), 401


# LOGOUT
@app.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message":"Logged in successfully!"})


# ADD Product
@app.route('/api/products/add', methods=["POST"])
@login_required
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"],price=data["price"],description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message":"Product added successfully!"})
    return jsonify({"message":"Invalid product data"}), 400


# DELETE Product
@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message":"Product deleted successfully!"})
    return jsonify({"message":"product not found"}), 404 
# vai Recuperar o produto da base de dados, Verificar se o produto existe, e se existe apagar da base de dados, mas se nao existe retorna erro (404)
     
@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
             "price": product.id,
             "description": product.description
        })
    return jsonify({"Product not found"}), 404


# SHOW list PRODUCTs (GET)
@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
            })
    return jsonify({"message": "Product not found"}), 404


# UPDATE Product (PUT) - Atualizar pruduto
@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    data = request.json
    if 'name' in data:
        product.name = data['name']

    data = request.json
    if 'price' in data:
        product.price = data['price'] 

    data = request.json
    if 'description' in data:
        product.description = data['description']   
    db.session.commit()
    return jsonify({'message': "Product update successfully"})


# TABLE PRODUCTS
@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list=[]
    for product in products:
        product_data={
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        }
        product_list.append(product_data)
        return jsonify(product_list)


# HOMEPAGE - Definir uma rota raiz (página inicial) e a função que será executada 
@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == "__main__":
    app.run(debug=True)

#criando o banco dados: new terminal: flask shell
#depois: db.create_all()
#depois: db.session.commit()
# a session é a conexao com o db, o commit efetiva as mudanças enviando para o banco dados
#por fim: exit()
#vai ser criado  a pasta instance, e o arquivo de extensao .db
