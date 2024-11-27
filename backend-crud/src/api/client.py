from flask import Blueprint, request
from capaNegocio.client_logic import Clients
from capaPersistencia.mongo_connection import mongo
from api.helpers import response

client_blueprint = Blueprint('client', __name__)

client_logic = Clients(mongo)


@client_blueprint.route('/client/<id>', methods = ['PUT'])
def update_client(id):
    try:
        client_data = {
            'shoppingCart': request.json.get('shoppingCart', [])
        }
        client_logic.update_client(id, client_data)
        return response(True, message="client updated", status=200)
    except Exception as e:
        return response(False, message=str(e), status=500)
        
