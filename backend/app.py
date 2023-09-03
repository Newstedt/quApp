from flask import Flask, request, Response
import flask
import json
from flask_cors import CORS
import numpy as np
import pandas as pd
import quandl
import plotly.express as px 
from datetime import datetime, timedelta
import fetchData
import calcPrice

#ustYields = fetchData.fetchSingleDayYield(datetime.today())

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "UST App Root"

@app.route('/users', methods=["GET", "POST"])
def users():
    print("users endpoint reached...")
    if request.method == "GET":
        with open("users.json", "r") as f:
            data = json.load(f)
            data.append({
                "username": "user4",
                "pets": ["hamster"]
            })

            return flask.jsonify(data)
    if request.method == "POST":
        received_data = request.get_json()
        print(f"received data: {received_data}")
        message = received_data['data']
        return_data = {
            "status": "success",
            "message": f"received: {message}"
        }
        return flask.Response(response=json.dumps(return_data), status=201)

@app.route('/ustYields', methods=["GET", "POST"])
def ustYields():
    print("ustYields endpoint reached...")
    if request.method == "GET":
        ustYields = fetchData.fetchSingleDayYield(datetime.today())
    elif request.method == "POST":
        received_date = request.get_json()
        input_date = received_date["yield date"]
        ustYields = fetchData.fetchSingleDayYield(datetime.strptime(input_date, "%Y-%m-%d"))
        
    return Response(ustYields.to_json(orient ='index'), mimetype='application/json')

@app.route('/ustCusips', methods=["GET"])
def ustCusips():
    print("ustCusips endpoint reached...")
    if request.method == "GET":
        ustCusips = fetchData.getCusipList()
    return Response(ustCusips)

@app.route('/bondCashflows', methods=["POST"])
def bondCashflows():
    print("bondCashflows endpoint reached...")
    if request.method == "POST":
        received_cusip = request.get_json()
        input_cusip = received_cusip['bond cusip']
        theoPrice, bondCashflows = calcPrice.theoPriceFromCusip(input_cusip)
        
        cf_json = bondCashflows.to_json(orient ='index')
        price_json = json.dumps({'theoPrice': theoPrice})
        merged_json = {**json.loads(price_json), **json.loads(cf_json)}
        
    return Response(merged_json, mimetype='application/json')

def getUstYields(yield_date):
    if not yield_date:
        t = datetime.today()
    else:
        t = datetime.strptime(yield_date, "%Y-%m-%d")
    
    ustYield = fetchData.fetchSingleDayYield(t)
        
    return ustYield.to_json(orient ='index')

if __name__ == "__main__":
    app.run("localhost", 6969)