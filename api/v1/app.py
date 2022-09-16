#!/usr/bin/python3
"""
starts a Flask web application
"""

from models import storage
from os import getenv
from api.v1.views import app_views
from flask import Flask
from flask import jsonify
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

@app.errorhandler(404)
def page_not_found():
    # note that we set the 404 status explicitly
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    if (getenv("HBNB_API_HOST") and getenv("HBNB_API_PORT")):
        api_host = getenv("HBNB_API_HOST")
        api_port = getenv("HBNB_API_PORT")
        app.run(host=api_host, port=api_port, threaded=True)
    else:
        app.run(host='0.0.0.0', port='5000', threaded=True)
