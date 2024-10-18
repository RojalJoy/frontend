from flask import Flask, request, jsonify
import json
from model import probe_model_5l_profit

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']  # Expecting file from the POST request
    data = json.load(file)
    result = probe_model_5l_profit(data["data"])
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
