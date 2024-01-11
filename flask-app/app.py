import flask
from pymongo import MongoClient

import os


mongo_uri = os.environ.get('MONGO_URI')
mongo_client = MongoClient(mongo_uri)

database = mongo_client.test
collection = database.restaurants

app = flask.Flask(__name__)



@app.route('/')
def index():
    data = collection.find_one()
    app.logger.info(type(data))
    print(type(data))

    return str(data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)