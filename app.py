import flask
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
import utils


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("main.html")


@app.route("/time")
def get_time():
    return utils.get_time()


@app.route("/centerA")
def get_centerA_data():
    data = utils.get_centerA_data()
    return jsonify({"confirm": int(data[0]),"suspect": int(data[1]),"heal": int(data[2]),"dead": int(data[3])})


@app.route("/centerB")
def get_centerB_data():
    res = []
    for tup in utils.get_centerB_data():
        print(tup)
        res.append({"name":tup[0],"value":int(tup[1])})
    return jsonify({"data":res})


@app.route("/detail")
def get_detail():
    return render_template("detail.html")


if __name__ == '__main__':
    app.run()
