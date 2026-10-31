from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fresh.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- DATABASE TABLE ---
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price}

# Create DB file
with app.app_context():
    db.create_all()
    # Add sample data only first time
    if not Product.query.first():
        db.session.add(Product(name="Peshawari Chappal", price=3500))
        db.session.add(Product(name="Waziri Cap", price=800))
        db.session.commit()

# --- ROUTES ---
@app.route('/')
def home():
    return {"message": "Fresh API LIVE with DATABASE - Danyal!"}

@app.route('/api/products')
def products():
    all_products = Product.query.all()
    return jsonify([p.to_dict() for p in all_products])

@app.route('/api/products/<int:id>')
def one_product(id):
    product = Product.query.get(id)
    if product:
        return jsonify(product.to_dict())
    return jsonify({"error": "Product not found"}), 404

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

if __name__ == '__main__':
    app.run(debug=True, port=5001)
else:
    with app.app_context():
        db.create_all()