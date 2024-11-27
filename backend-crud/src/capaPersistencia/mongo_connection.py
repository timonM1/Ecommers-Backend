from flask_pymongo import PyMongo

mongo = PyMongo()

def set_mongo(app):
    mongo.init_app(app)