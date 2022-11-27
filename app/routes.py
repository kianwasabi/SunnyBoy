from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
from database.models import *
import socket

hostname = socket.gethostname()
hostIP = socket.gethostbyname(hostname)

def create_message(key:str, decive:str, data:dict):
    '''
    Template function that creates the REST APIs Response/Request Message.
    Parameter:
    key (str) -> Process Key
    decive (str) -> Client/Server ID
    data (dict) -> Payload
    '''
    message = {
        "Header": {
            "Key": key, 
            "Device": decive,
            "TimeStamp": datetime.now()
        },
        "Data": {
            data
        }
    }
    if (key[1] == 1):#1:Request
        message["RequestData"] = message.pop("Data")
    if (key[1] == 2):#2:Respone   
        message["ResponseData"] = message.pop("Data")
    return message

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/api')
def api():
    return render_template("api.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/api/requestrecipe/', methods = ['POST'])
def api_requestrecipe():
    #receive data from client
    api_data = request.get_json() 

    #message back
    key = "0120"
    device = hostIP
    #data = functionxY
    message = create_message(key,device,data)
    return jsonify(message)

@app.route('/api/post/weatherinformation/refresh', methods=['POST'])
def api_post_weatherinformation_refresh():
    #if request.method == 'POST':
    refresh_weatherinformation()
    key = "1120"
    device = hostIP
    data = {
        "Response": f"Weatherinformation refreshed at: {datetime.now()}"
    }
    response_message = create_message(key,device,data)
    return jsonify(response_message) 

@app.route('/api/get/weatherinformation/all', methods=['GET'])
def api_get_weatherinformation_all():
    key = "1110"
    device = hostIP
    data = get_current_weatherinformation()
    message = create_message(key,device,data)
    return jsonify(message)

@app.route('/api/get/sun/position', methods=['GET'])
def api_get_sun_position():
    sunposition = get_current_sunposition()
    key = "2110" 
    device = hostIP
    data = {
        "Azimuth": sunposition[0],
        "Elevation": sunposition[1]
    }
    message = create_message(key,device,data)
    return jsonify(message)

@app.route('/api/post/solarpanel/position', methods=['POST'])
def api_post_solarpanel_position():
    #receive data from client
    api_data = request.get_json()
    value1 = api_data['RequestData']['Value1']
    value2 = api_data['RequestData']['Value2'] 
    #post data into database
    post_panelposition(value1,value2)
    #respone client
    key = "2220"
    device = hostIP
    data = {"Response": "Values saved to database"}
    message = create_message(key,device,data)
    return jsonify(message)

