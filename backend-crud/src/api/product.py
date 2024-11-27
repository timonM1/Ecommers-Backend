from flask import Blueprint, request
from capaNegocio.product_logic import Products
from capaPersistencia.mongo_connection import mongo
from api.helpers import response

product_blueprint = Blueprint('products', __name__)

product_logic = Products(mongo)

@product_blueprint.route('/products', methods=['GET'])
def get_all_products():
    try:
        products = [
            {
                '_id': str(product['_id']),
                'name': product['name'],
                'description': product.get('description', 'without description'),
                'attributes': product.get('attributes', 'without attributes'),
                'price': product['price'],
                'stock': product['stock'],
                'category_id': product.get('id_category', 'without category'),
            }
            for product in product_logic.get_all_products()
        ]
        return response(True, products, "Products retrieved successfully", 200)
    except Exception as e:
        return response(False, message=str(e), status=500)

@product_blueprint.route('/products/<id>', methods=['GET'])
def get_product(id):
    try:
        product = product_logic.get_product(id)
        if product:
            product_data = {
                '_id': str(product['_id']),
                'name': product['name'],
                'description': product['description'],
                'attributes': product.get('attributes', 'without attributes'),
                'price': product['price'],
                'stock': product['stock']
            }
            return response(True, product_data, "Product found", 200)
        else:
            return response(False, message="Product not found", status=404)
    except Exception as e:
        return response(False, message=str(e), status=500)

@product_blueprint.route('/products', methods=['POST'])
def create_product():
    try:
        product_data = request.json
        new_product = product_logic.add_product(product_data)
        return response(True, new_product, "Product created", 201)
    except Exception as e:
        return response(False, message=str(e), status=400)

@product_blueprint.route('/products/<id>', methods=['PUT'])
def update_product(id):
    try:
        product_data = {
            'name': request.json.get('name'),
            'description': request.json.get('description'),
            'price': request.json.get('price'),
            'stock': request.json.get('stock'),
            'attributes': request.json.get('attributes', []),
        }
        updated = product_logic.update_product(id, product_data)
        if updated:
            return response(True, message="Product updated", status=200)
        else:
            return response(False, message="Product not found", status=404)
    except Exception as e:
        return response(False, message=str(e), status=500)

@product_blueprint.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    try:
        deleted = product_logic.delete_product(id)
        if deleted.deleted_count > 0: 
            return response(True, message="Product deleted", status=200)
        else:
            return response(False, message="Product not found", status=404)
    except Exception as e:
        print("Error:", e)
        return response(False, message=str(e), status=500)
