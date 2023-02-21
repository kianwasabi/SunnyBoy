from flask import Flask,  make_response , request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
from database.models import *
from config import *
import subprocess

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ------ web interface routes ------
@app.route('/', methods=["POST","GET"])
def home():
    if request.method == "POST":
        location = request.form["location"]
        device = request.headers["Host"]
        set_weatherinformation(location,device)
        weatherinfo = get_current_weatherinformation()
        return render_template("home.html",data=weatherinfo)        
    else: 
        weatherinfo = get_current_weatherinformation()
        return render_template("home.html",data=weatherinfo)

@app.route('/shutdown')
def shutdown():
    #restart
    #subprocess.run("shutdown -r 0", shell=True, check=True)
    #shutdown
    subprocess.run("shutdown -h 0", shell=True, check=True)
    return "Shuting down server ... "

@app.route('/api')
def api():
    return render_template("api.html")

@app.route('/processcontrol', methods=["POST","GET"])
def processcontrol(): 
    print(get_devices())
    return render_template("processcontrol.html")   
        
@app.route('/about')
def about():
    return render_template("about.html")
# ------ device routes ------
def message_in_Terminal(message):
    print("╔════════════════════════════════════════════════════════════════╗")
    print(message.headers)
    print(message.text)
    print("╚════════════════════════════════════════════════════════════════╝")

def api_response(key:str, res_data:dict):
    '''
    Creates the REST APIs response message.
    :param key: (str) Process Key
    :param decive: (str) Server IP
    :param data: (dict) Payload
    :return: (*args: Any) -> Response 
    '''
    response = make_response(jsonify(res_data))
    response.headers.add("Key",key)
    response.headers.add("Host",f"{hostIP}:{port}")
    #response.headers.add("Port",port)
    message_in_Terminal(response)
    return response

def api_request():
    '''
    Handels the REST APIs request message.
    :param key: none
    :return req_data: (dict) payload in JSON object
    :return device: (str) Device IP = device_id in DB
    :return key: (str) Process Key
    '''
    req_data = request.get_json()
    device = request.headers["Host"]
    key = request.headers["Key"]
    message_in_Terminal(request)
    return req_data, device, key

@app.route('/api/post/requestrecipe/', methods = ['POST'])
def api_requestrecipe():
    # http request
    req_data, device, key = api_request()
    # server operation
    recipe = get_recipe_by_device_id(device)
    # http response 
    res_data = {
        "Response_Data":recipe
    }
    response = api_response(key,res_data)
    return response

@app.route('/api/post/weatherinformation/refresh', methods=['POST'])
def api_post_weatherinformation():
    # http request
    req_data, device, key = api_request()
    cityname = req_data["Request_Data"]["Location"]
    # server operation
    _, time_refreshed = set_weatherinformation(cityname,device)
    # http response 
    res_data = {
        "Response_Data": 
            {"Status": f"Weatherinformation for {cityname} saved in database at {time_refreshed}."}
    }
    response = api_response(key,res_data)
    return response

@app.route('/api/get/weatherinformation/all', methods=['GET'])
def api_get_weatherinformation_all():
    # http request
    req_data, device, key = api_request()
    # server operation 
    current_weather = get_current_weatherinformation()
    # http response 
    res_data = {
        "Response_Data": current_weather
    }
    response = api_response(key,res_data)
    return response

@app.route('/api/get/sun/position', methods=['GET'])
def api_get_sun_position():
    # http request
    req_data, device, key = api_request()
    # server operation 
    sunposition = get_current_sunposition()
    # http response 
    res_data = {
        "Response_Data": sunposition
    }
    response = api_response(key,res_data)
    return response

@app.route('/api/post/solarpanel/position', methods=['POST'])
def api_post_solarpanel_position():
    # http request
    req_data, device, key = api_request()
    value1 = req_data['Request_Data']['Value1']
    value2 = req_data['Request_Data']['Value2'] 
    # server operation - 
    _, time_saved = post_panelposition(value1,value2)
    # http response 
    res_data = {
        "Response_Data": 
        {
            "Status": f"Values saved to database: {time_saved}"
        }
    }
    response = api_response(key,res_data)
    return response