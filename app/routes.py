from flask import Flask, request, jsonify
from flask_cors import CORS

from database.db import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():   
    return "Hello"

@app.route('/api/sunpositions', methods=['GET'])
def api_get_sunpositions():
    return jsonify(get_sunpositions())

@app.route('/api/sunpositions/<sid>', methods=['GET'])
def api_get_sunposition(sid):
    return jsonify(get_sunposition_by_sid(sid))

@app.route('/api/sunpositions/add',  methods = ['POST'])
def api_add_sunposition():
    sunposition = request.get_json()
    return jsonify(insert_sunposition(sunposition))

@app.route('/api/sunpositions/update',  methods = ['PUT'])
def api_update_sunposition():
    sunposition = request.get_json()
    return jsonify(update_sunposition(sunposition))

@app.route('/api/sunpositions/delete/<sid>',  methods = ['DELETE'])
def api_delete_sunposition(sid):
    return jsonify(delete_sunposition(sid))

