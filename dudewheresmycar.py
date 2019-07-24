# curl http://parking.dudewheresmycar.com.br/park -d "floor=3&location=The One&spot=None" -X POST -v
# curl http://parking.dudewheresmycar.com.br/parked
# http://flask-restful.readthedocs.io/en/latest/quickstart.html

import json

from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse

class Persistance():
    def __init__(self):
        self.filename = '/var/www/dudewheresmycar/dudewheresmycar.json'

    def save(self, park):
        with open(self.filename, 'w') as perFile:
            perFile.write(json.dumps(park))

    def open(self):
        with open(self.filename, 'r') as perFile:
            return perFile.read()

class Parked(Resource):
    def get(self):
        park = json.loads(persistance.open())
        response = Response(
            response='<html><title>Car is parked at</title><style> tab1 { padding-left: 4em; }</style><body><p><tab1>Floor: %s</tab1></p><p><tab1>Location: %s</tab1></p><p><tab1>Spot: %s</tab1></p></body></html>' % (park['floor'], park['location'], park['spot']),
            #json.dumps(park),
            status=200)
        return response

class Park(Resource):
    def post(self):
        args = parser.parse_args()
        park = {}
        park['floor'] = args['floor']
        park['location'] = args['location']
        park['spot'] = args['spot']
        persistance.save(park)
        return "OK", 201

application = Flask(__name__)
api = Api(application)

parser = reqparse.RequestParser()
parser.add_argument('floor')
parser.add_argument('location')
parser.add_argument('spot')

persistance = Persistance()

api.add_resource(Park, '/park')
api.add_resource(Parked, '/parked')

if __name__ == '__main__':
    application.run(debug=True)

