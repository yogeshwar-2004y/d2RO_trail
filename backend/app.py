from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api')
def hello_world():
    return jsonify(message="Hello from Flask!")

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, jsonify

# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return jsonify(message="Hello from Flask!")

# if __name__ == '__main__':
#     app.run(debug=True)
