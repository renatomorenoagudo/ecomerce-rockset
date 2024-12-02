#importação
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

# Modelagem
# Produto(id, name, price, description)
# Definir uma rota raiz (página inicial) e a função que será executada ao requisitar
@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == "__main__":
    app.run(debug=True)