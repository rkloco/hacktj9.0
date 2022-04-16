from flask import Flask, send_from_directory, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
from myapi.CoordinateHandler import CoordinateHandler

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app) #comment this on deployment
api = Api(app)

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

#@app.route('/', defaults={'path':''})
#def get_city():
    #return request.args.get('name')

my_city = 'Taj Mahal, Agra, Uttar Pradesh 282001'
api.add_resource(CoordinateHandler, '/flask/hello', resource_class_kwargs={'city': my_city})