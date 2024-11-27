from flask import Blueprint
from capaPersistencia.mongo_connection import mongo
from capaNegocio.category_logic import Categorias
from api.helpers import response

categories_blueprint = Blueprint('categories', __name__)

categoria = Categorias(mongo)

@categories_blueprint.route('/categories', methods=['GET'])
def get_all_categories():
    try:
        categorias_data = categoria.get_all_categories()
        categories = [
            {
                '_id': str(categoria['_id']),
                'name': categoria['nombre'],
            } for categoria in categorias_data
        ]
        return response(True, data=categories, message="Categorías obtenidas")
    except Exception as e:
        return response(False, message=str(e), status=400)
