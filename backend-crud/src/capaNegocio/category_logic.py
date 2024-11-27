class Categorias():
    def __init__(self, mongo):
        self.mongo = mongo
    
    def get_all_categories(self):
        return list(self.mongo.db.categorias.find())