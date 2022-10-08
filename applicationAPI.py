from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello'

#run every time after closing the terminal
#export FLASK_APP=applicationAPI
#export FLASK_ENV=development
#flask run