#!/usr/bin/env python

"""Flask REST API server for NLP parser"""

import requests
from flask_restful import Resource
from flask import request
from parser.util import parse_text
from parser.api.setup import api, app
import parser.api.definitions

class NLP(Resource):
    def post(self):
        """
        Parse Question
        ---
        tags: [parse]
        summary: "Convert a natural-language question into machine-readable form."
        requestBody:
            name: "question"
            description: "Natural-language question"
            required: true
            content:
                text/plain:
                    schema:
                        type: string
                        example: "What genes affect Ebola?"
        responses:
            200:
                description: "Here's your graph"
                schema:
                    $ref: "#/definitions/Graph"
            400:
                description: "Something went wrong"
        """
        string = request.get_data().decode() # convert bytes to normal str
        if string[0] == string[-1] == "\"":
            string = string[1:-1]
        graph = parse_text(string)
        
        return graph, 200

api.add_resource(NLP, '/parse/')

if __name__ == '__main__':

    # Get host and port from environmental variables
    server_host = '0.0.0.0'
    server_port = 9475

    app.run(host=server_host,\
        port=server_port,\
        debug=True,\
        use_reloader=True)
