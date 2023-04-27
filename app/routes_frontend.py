from flask import request, render_template
from database.models import *
from config import *
from .server import *

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