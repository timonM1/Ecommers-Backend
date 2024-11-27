class Orders():
    def __init__(self, mongo):
        self.mongo = mongo
    
    def create_order(self, order_data):
        try:
            
            if self.mongo is None:
                raise ValueError("No se pudo conectar a MongoDB")

            result = self.mongo.db.pedidos.insert_one(order_data)
            return result
        except Exception as e:
            print("Error al insertar el pedido en MongoDB:", str(e))
            raise e 