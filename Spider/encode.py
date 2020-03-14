from json.encoder import MyJSONEncoder

import flask
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
import utils


# app = Flask(__name__)
app = flask.Flask(...)
app.json_encoder = MyJSONEncoder


@app.route('/')
def hello_world():
    return render_template("main.html")


@app.route("/time")
def get_time():
    return utils.get_time()


@app.route("/centerA")
def get_centerA_data():
    data = utils.get_centerA_data()
    return jsonify({"confirm": data[0],"suspect": data[1],"heal": data[2],"dead": data[3]})


if __name__ == '__main__':
    app.run()
