from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from geopy.geocoders import Nominatim
import random
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import torch
import torch.nn as nn

import torch
import torch.nn as nn

import pandas as pd
import requests
import json

class NueralNet(nn.Module):
    def __init__(self):
        super(NueralNet, self).__init__()
        self.rnn = nn.GRU(3, 35, 3)
        self.linear = nn.Linear(35, 1)
    def forward(self, X, state):
        X, _ = self.rnn(X, state)
        return self.linear(X)

model = NueralNet()
_ = model(torch.zeros(58, 1, 3), torch.zeros(3, 1, 35))
model.load_state_dict(torch.load("myapi/model.pt", map_location=torch.device('cpu')))


import numpy as np
import netCDF4
from math import pi
from numpy import cos, sin
from scipy.spatial import cKDTree

"""
How these files work is that each file has three variables of interest: lat, lon, mssh.
mssh is mean sea surface height change (sea level change). All of these variables are basically
numpy arrays of size like 600,000. Since they're all the same size, you can query by index, so
the element at a certain index of the latitude array corresponds to the element at the same index from
both the longitude and mssh arrays, so that way it's easy to get data by coordinates
"""

def get_elevation(lat, long):
    query = ('https://api.open-elevation.com/api/v1/lookup'
        f'?locations={lat},{long}')
    elevation = pd.json_normalize(requests.get(query).json(), 'results')['elevation'].values[0]
    return elevation*304.8

def kdtree_fast(latvar,lonvar,lat0,lon0): # This basically returns the closest dataset point to the inputted coordinates
    rad_factor = pi/180.0 # for trignometry, need angles in radians
    # Read latitude and longitude from file into numpy arrays
    latvals = latvar[:] * rad_factor
    lonvals = lonvar[:] * rad_factor
    clat, clon = cos(latvals), cos(lonvals)
    slat, slon = sin(latvals), sin(lonvals)

    # Build kd-tree from big arrays of 3D coordinates
    triples = list(zip(np.ravel(clat*clon), np.ravel(clat*slon), np.ravel(slat)))
    kdt = cKDTree(triples)

    lat0_rad = lat0 * rad_factor
    lon0_rad = lon0 * rad_factor
    clat0,clon0 = cos(lat0_rad),cos(lon0_rad)
    slat0,slon0 = sin(lat0_rad),sin(lon0_rad)

    dist_sq_min, minindex_1d = kdt.query([clat0*clon0, clat0*slon0, slat0])
    i = np.unravel_index(minindex_1d, latvals.shape)
    return i,i

def get_prediction(data_tensor, model, close_lat, close_lon):
  x = np.arange(3986, 4045)/2
  y = data_tensor
  n = np.size(x)
  
  x_mean = np.mean(x)
  y_mean = np.mean(y)
  x_mean,y_mean
  
  Sxy = np.sum(x*y)- n*x_mean*y_mean
  Sxx = np.sum(x*x)-n*x_mean*x_mean
  
  b1 = Sxy/Sxx
  b0 = y_mean-b1*x_mean
  return b1, b0, x, y #intercept is b0, slope is b1
  
  
  


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
    elev = get_elevation(location.latitude, location.longitude)
    
    

    N = 5
    data_tensor = torch.load("myapi/tensor.pt")
    latvar = np.array([elem[0][1] for elem in data_tensor.permute(1,0,2)])
    
    lonvar = np.array([elem[0][2] for elem in data_tensor.permute(1,0,2)])
    
    i,j = kdtree_fast(latvar, lonvar, location.longitude, location.latitude)
      
    
     # Wichita coordinates, seems to be 2 degrees off
    close_lat, close_lon = latvar[i], lonvar[j]
    data_tensor = data_tensor.permute(1, 0 , 2)[i]
    print(i)
    X = np.array([data[0] for data in data_tensor])
    X+= X[-1]
    
    slope, intercept, x, y = get_prediction(X, model, close_lat, close_lon)
    y_pred = slope * x + intercept
    
    low_thres = elev-1000
    medium_thres = elev-350
    high_thres = elev-75
    submersion = elev
    
    low_year = round((low_thres-intercept)/slope)
    med_year = round((medium_thres-intercept)/slope)
    high_year = round((high_thres-intercept)/slope)
    sub_year = round((submersion-intercept)/slope)


    if low_year<2022: low_year = "Already here" 
    plt.scatter(x, y, color = 'red')
    plt.plot(x, y_pred, color = 'green')
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
      'img': base64_bytes.decode(),
      'lowyear': str(low_year),
      'medyear': str(med_year),
      'highyear': str(high_year),
      'subyear': str(sub_year)
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