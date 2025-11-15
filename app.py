from flask import Flask, request, jsonify, abort
import argparse
import requests
import json
from datetime import datetime
from email.utils import parsedate_to_datetime
import hashlib

app = Flask(__name__)

ports = ['9527', '9528', '9529']
data_store = {}

def hash_str_to_port(s):
    encoded = s.encode('utf-8')
    hash_digest = hashlib.sha256(encoded).hexdigest()
    big_int = int(hash_digest, 16)
    return big_int % 3 + 9527

@app.route('/', methods=['POST'])
def write_data():
    if not request.is_json:
        abort(400, description="Content-Type must be application/json")
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            abort(400, description="JSON body must be an object")

        for item in data:
            key, value = item, data[item]
        
        hash_port = hash_str_to_port(key)
        
        if hash_port == args.port:
            data_store[key] = value
        else:
            BASE_URL = f"http://cache-server-{hash_port}:{hash_port}/init_write_data"
            response = requests.post(
                BASE_URL,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(data)
            )
        return '', 200  
    except Exception as e:
        abort(400, description=str(e))
        
@app.route('/init_write_data', methods=['POST'])
def init_write_data():
    if not request.is_json:
        abort(400, description="Content-Type must be application/json")
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            abort(400, description="JSON body must be an object")
        data_store.update(data)
        return '', 204  
    except Exception as e:
        abort(400, description=str(e))

@app.route('/<key>', methods=['GET'])
def read_data(key):
    hash_port = hash_str_to_port(key)
    value = ""
    if hash_port == args.port:
        if key in data_store:
            value = data_store[key]
    else:
        BASE_URL = f"http://cache-server-{hash_port}:{hash_port}/init_read_data/{key}"
        response = requests.get(
            BASE_URL,
            headers={'Content-Type': 'application/json'},
        )
        content = response.json() 
        if content != "":
            value = content

    if value != "":
        return jsonify({key: value})
    else:
        return '', 404

@app.route('/init_read_data/<key>', methods=['GET'])
def init_read_data(key):
    if key in data_store:
        return jsonify(data_store[key])
    else:
        return jsonify('')

@app.route('/<key>', methods=['DELETE'])
def delete_data(key):
    flag = False
    hash_port = hash_str_to_port(key)
    if hash_port == args.port:
        if key in data_store:
            flag = True
            data_store.pop(key)
    else:
        BASE_URL = f"http://cache-server-{hash_port}:{hash_port}/init_delete_data/{key}"
        response = requests.delete(
            BASE_URL,
            headers={'Content-Type': 'application/json'}
        )
        content = response.json()
        if content:
            flag = True
    if flag:
        return jsonify(1)
    else:
        return jsonify(0)

@app.route('/init_delete_data/<key>', methods=['DELETE'])
def init_delete_data(key):
    if key in data_store:
        data_store.pop(key)
        return jsonify(True)   
    else:
        return jsonify(False)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the key-value store service.")
    parser.add_argument('--port', type=int, default=5000, help="Port to listen on (default: 5000)")

    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port, debug=True)