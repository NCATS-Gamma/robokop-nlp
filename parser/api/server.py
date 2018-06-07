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
        parameters:
          - in: "body"
            name: "question"
            description: "Natural-language question"
            required: true
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
        graph = parse_text(request.json)
        # try:
        #     graph = parse_text(request.json)
        # except Exception as err:
        #     return f"Failed to parse question. {err}", 500
        
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
