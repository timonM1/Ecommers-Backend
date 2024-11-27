import sys
import os
from flask import Flask, jsonify, send_from_directory, redirect
from flask_cors import CORS
from dotenv import load_dotenv
from api.product import product_blueprint
from api.category import categories_blueprint
from api.client import client_blueprint
from api.order import order_blueprint
from capaPersistencia.mongo_connection import set_mongo

# Modificar sys.path antes de importar cualquier módulo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Inicializar la app Flask
app = Flask(__name__)

# Configuración de variables de entorno
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
if not app.config['MONGO_URI']:
    raise RuntimeError("MONGO_URI no está configurado. Verifica tus variables de entorno.")
print(f"MONGO_URI cargada: {app.config['MONGO_URI']}")

# Inicializar MongoDB desde la capa de persistencia
set_mongo(app)

# Habilitar CORS
CORS(app)

# Registrar blueprints
app.register_blueprint(product_blueprint)
app.register_blueprint(categories_blueprint)
app.register_blueprint(client_blueprint)
app.register_blueprint(order_blueprint)

# Ruta para servir el frontend React (redirige a GitHub Pages)
@app.route('/crud-db-ecommers/')
def serve_react():
    return redirect("https://<tu-github-username>.github.io/<tu-repo>/", code=302)

# Rutas no encontradas (fallback al frontend React)
@app.errorhandler(404)
def not_found(e):
    return redirect("https://<tu-github-username>.github.io/<tu-repo>/", code=302)

@app.route('/home')
def home():
    return jsonify({"message": "Bienvenido a la API"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)), debug=True)
