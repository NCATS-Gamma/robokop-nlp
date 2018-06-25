'''
Set up Flask server
'''

import os
import sys

from flask import Flask, Blueprint
from flask_restful import Api
from flasgger import Swagger
from flask_cors import CORS

app = Flask(__name__)

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint)
CORS(app)
app.register_blueprint(api_blueprint)

template = {
    "openapi": "3.0.1",
    "info": {
        "title": "ROBOKOP NLP Parser",
        "description": "An API for parsing natural-language biomedical questions",
        "contact": {
            "responsibleOrganization": "NCATS Gamma",
            "responsibleDeveloper": "patrick@covar.com",
            "email": "patrick@covar.com",
            "url": "github.com/ncats-gamma",
        },
        "termsOfService": "<url>",
        "version": "0.0.1"
    },
    "schemes": [
        "http",
        "https"
    ]
}
app.config['SWAGGER'] = {
    'title': 'ROBOKOP NLP Parser API',
    'uiversion': 3
}
swagger = Swagger(app, template=template)