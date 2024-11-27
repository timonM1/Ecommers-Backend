from flask_pymongo import  ObjectId
class Clients:
    def __init__(self, mongo):
        self.mongo = mongo
    
    def update_client(self, client_id, client_data):
        print(client_data)
        current_cart = self.mongo.db.clientes.find_one({'_id': ObjectId(client_id)}).get('shoppingCart', [])
        
        # Productos a agregar o actualizar
        updated_cart = current_cart

        for new_product in client_data['shoppingCart']:
            product_found = False
            for product in updated_cart:
                if product['name'] == new_product['name']: 
                    product['quantity'] += new_product['quantity']
                    product['total'] += new_product['total'] 
                    product_found = True
                    break

            if not product_found:
                updated_cart.append(new_product)

        result = self.mongo.db.clientes.update_one(
            {'_id': ObjectId(client_id)},
            {'$set': {'shoppingCart': updated_cart}}
        )
        return result
        
    