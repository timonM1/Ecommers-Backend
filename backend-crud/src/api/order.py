from flask import Blueprint, request
from capaNegocio.order_logic import Orders
from capaPersistencia.mongo_connection import mongo
from api.helpers import response
from datetime import datetime
import pytz

order_blueprint = Blueprint('order', __name__)

order_logic = Orders(mongo)


@order_blueprint.route('/order', methods = ['POST'])
def create_order():
    try:
        print(request.json) 
        cart_items = request.json.get('cartItems', [])
        total = sum(item['total'] for item in cart_items)
        
        chile_tz = pytz.timezone('Chile/Continental')
        fecha_chile = datetime.now(chile_tz)
    
        order_data = {
            'clienteId': request.json.get('clientId'), 
            'productos': cart_items,  
            'fecha': fecha_chile,
            'total': total  
        }
        order_logic.create_order(order_data)
        return response(True, message="order created", status=200)
    except Exception as e:
        return response(False, message=str(e), status=500)
        
