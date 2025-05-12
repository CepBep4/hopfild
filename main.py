from flask import Flask, render_template, jsonify
from neuro import learn_and_test

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/pres')
def pres():
    return render_template("pres.html")

@app.route("/getPhotos")
def getPhotos():
    return jsonify(learn_and_test())

@app.after_request
def allow_everyone(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    return response

if __name__ == "__main__":
    app.run(debug=True, port=6600, host="0.0.0.0")