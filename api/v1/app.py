#!/usr/bin/python3
"""script that starts a Flask web api"""
from flask import Flask, Blueprint
from flask_cors import CORS

from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(error):
    """close"""

    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    return {
        "error": "Not found"
    }, 404


if __name__ == "__main__":
    """main function"""

    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = 5000
    app.run(host=host, port=port, threaded=True)
