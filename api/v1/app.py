#!/usr/bin/python3
"""
starts a Flask web application
"""

from models import storage
from os import getenv
import api.v1.views from app_views
from flask import Flask
app = Flask(__name__)

@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == '__main__':
    if (getenv("HBNB_API_HOST") and getenv("HBNB_API_PORT")):
        api_host = getenv("HBNB_API_HOST")
        api_port = getenv("HBNB_API_PORT")
        app.run(host=api_host, port=api_port)
    else:
        app.run(host='0.0.0.0', port='5000')

