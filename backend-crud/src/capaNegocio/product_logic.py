from flask_pymongo import  ObjectId

class Products:
    def __init__(self, mongo):
        self.mongo = mongo

    def add_product(self, product_data):
        # Validar que el stock sea al menos 1
        if product_data.get('stock', 1) < 1:
            raise ValueError("El stock no puede ser menor que 1.")

        # Validar que el precio no sea negativo
        if product_data.get('price', 0) < 0:
            raise ValueError("El precio no puede ser negativo.")

        result = self.mongo.db.productos.insert_one(product_data)
        nuevo_producto = self.mongo.db.productos.find_one({'_id': result.inserted_id})
        nuevo_producto['_id'] = str(nuevo_producto['_id'])

        return nuevo_producto
        

    def get_all_products(self):
        return list(self.mongo.db.productos.find())

    def get_product(self, product_id):
        return self.mongo.db.productos.find_one({'_id': ObjectId(product_id)})

    def update_product(self, product_id, product_data):
        if product_data.get('stock', 1) < 1:
            raise ValueError("El stock no puede ser menor que 1.")

        if product_data.get('price', 0) < 0:
            raise ValueError("El precio no puede ser negativo.")
        
        result = self.mongo.db.productos.update_one(
            {'_id': ObjectId(product_id)},
            {'$set': product_data}         
        )
        if result.matched_count == 0:
            print(f"No document found with ID: {product_id}")
        if result.modified_count == 0:
            print(f"Document found, but no fields were modified.")
        return result

    def delete_product(self, product_id):
        return self.mongo.db.productos.delete_one({'_id': ObjectId(product_id)})