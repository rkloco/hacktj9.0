from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from geopy.geocoders import Nominatim
import random
import matplotlib.pyplot as plt
import numpy as np
import mpld3
import io
import base64

class CoordinateHandler(Resource):
  def __init__(self):
    self.my_city = request.args.get('name')
  
  def get(self):
    #address we need to geocode
    loc = self.my_city
    #making an instance of Nominatim class
    geolocator = Nominatim(user_agent="my_request")
    
    #applying geocode method to get the location
    location = geolocator.geocode(loc)
    
    #printing address and coordinates
    msg = str(location.latitude) + ', ' + str(location.longitude)
    N = 5
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([3, 4, 5, 2, random.randint(1, 5)])
    colors = np.array(['black']*5)
    #area = (30 * np.random.rand(N))**2  # 0 to 15 point radii
    area = 4

    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    #saveloc = '../../scatter0.png'
    #plt.savefig(saveloc)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    base64_bytes = base64.b64encode(buf.read())
    #retf = mpld3.fig_to_html(f)
    plt.close()
    return {
      'resultStatus': 'SUCCESS',
      'message': msg,
      'num': '5',
      'img': base64_bytes.decode()
      }

  def post(self):
    print(self)
    parser = reqparse.RequestParser()
    parser.add_argument('type', type=str)
    parser.add_argument('message', type=str)

    args = parser.parse_args()

    print(args)
    # note, the post req from frontend needs to match the strings here (e.g. 'type and 'message')

    request_type = args['type']
    request_json = args['message']
    # ret_status, ret_msg = ReturnData(request_type, request_json)
    # currently just returning the req straight
    ret_status = request_type
    ret_msg = request_json

    if ret_msg:
      message = "Your Message Requested: {}".format(ret_msg)
    else:
      message = "No Msg"
    
    final_ret = {"status": "Success", "message": message}

    return final_ret