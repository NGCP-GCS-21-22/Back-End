from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/get_name', methods=['GET', 'POST'])
def get_name():
    input = request.get_json()
    return jsonify(input)

if __name__ == '__main__':
    app.run(debug=True)
