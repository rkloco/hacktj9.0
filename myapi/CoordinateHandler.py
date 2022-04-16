from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from geopy.geocoders import Nominatim

class CoordinateHandler(Resource):
  def __init__(self, city):
    self.my_city = city
  
  def get(self):
    #address we need to geocode
    #loc = 'Taj Mahal, Agra, Uttar Pradesh 282001'
    loc = self.my_city
    #making an instance of Nominatim class
    geolocator = Nominatim(user_agent="my_request")
    
    #applying geocode method to get the location
    location = geolocator.geocode(loc)
    
    #printing address and coordinates
    msg = str(location.latitude) + ', ' + str(location.longitude)
    return {
      'resultStatus': 'SUCCESS',
      'message': msg
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