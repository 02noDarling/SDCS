from flask import Flask, request, jsonify, abort
import argparse
import requests
import json

app = Flask(__name__)

ports = ['9527', '9528', '9529']
data_store = {}

@app.route('/', methods=['POST'])
def write_data():
    if not request.is_json:
        abort(400, description="Content-Type must be application/json")
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            abort(400, description="JSON body must be an object")
        
        for port in ports:
            BASE_URL = f"http://127.0.0.1:{port}/init_write_data"
            response = requests.post(
                BASE_URL,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(data)
            )
            if response.status_code != 204:
                abort(400, description={response.text})
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
    if key in data_store:
        return jsonify({key: data_store[key]})
    else:
        return '', 404

@app.route('/<key>', methods=['DELETE'])
def delete_data(key):
    flag = False
    if key in data_store:
        flag = True
    for port in ports:
        BASE_URL = f"http://127.0.0.1:{port}/init_delete_data/{key}"
        response = requests.delete(
            BASE_URL,
            headers={'Content-Type': 'application/json'}
        )
    if flag:
        return jsonify(1)
    else:
        return jsonify(0)

@app.route('/init_delete_data/<key>', methods=['DELETE'])
def init_delete_data(key):
    if key in data_store:
        data_store.pop(key)
    return '', 200

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the key-value store service.")
    parser.add_argument('--port', type=int, default=5000, help="Port to listen on (default: 5000)")

    args = parser.parse_args()
    app.run(host='127.0.0.1', port=args.port, debug=True)