from flask import Flask, jsonify, request, render_template
import os

app = Flask(__name__)

data = [
    {"id": 1, "name": "Peshawari Chappal", "price": 3500, "emoji": "🥿"},
    {"id": 2, "name": "Waziri Cap", "price": 800, "emoji": "🧢"},
    {"id": 3, "name": "Kohati Chappal", "price": 4200, "emoji": "👞"}
]

@app.route('/')
def home():
    return {"message": "Danyal PRO API - LIVE ONLINE!"}

@app.route('/api/products')
def products():
    return jsonify(data)

@app.route('/api/products', methods=['POST'])
def add_product():
    new_product = request.get_json()
    new_product["id"] = len(data) + 1
    new_product["emoji"] = "✨"
    data.append(new_product)
    return jsonify(new_product), 201

@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    global data
    data = [p for p in data if p["id"] != id]
    return jsonify({"message": "Deleted"})

@app.route('/shop')
def shop():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)