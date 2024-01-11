import flask
from pymongo import MongoClient

import os


mongo_uri = os.environ.get('MONGO_URI')
mongo_client = MongoClient(mongo_uri)

database = mongo_client.las

app = flask.Flask(__name__)

@app.route('/')
def index():
    all_collections = database.list_collection_names()
    num_doc_per_collection = { collection: database[collection].count_documents({}) for collection in all_collections }
    
    return str(num_doc_per_collection)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)