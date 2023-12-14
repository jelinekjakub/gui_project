import pymongo
from extensions.env import Config
mongo_client = pymongo.MongoClient("mongodb://admin:admin@mongodb:27017", connect=False)
db = mongo_client['app']

db.drop_collection('recipes')
db.drop_collection('users')

users_db = db['users']
recipes_db = db['recipes']