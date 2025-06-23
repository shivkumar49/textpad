from flask import Flask, request, jsonify, render_template
import os
import json

app = Flask(__name__)

DATA_FILE = 'user_data.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    content = request.get_json()
    password = content.get('password')
    user_data = content.get('data')

    if not password or not user_data:
        return 'Missing password or data', 400

    data = load_data()
    data[password] = user_data
    save_data(data)
    return 'Data saved successfully!'

@app.route('/retrieve', methods=['POST'])
def retrieve():
    content = request.get_json()
    password = content.get('password')

    if not password:
        return jsonify(success=False, message='Password is required'), 400

    data = load_data()
    if password in data:
        return jsonify(success=True, data=data[password])
    else:
        return jsonify(success=False, message='No data found for this password')

if __name__ == '__main__':
    app.run(debug=True)
