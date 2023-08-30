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

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello, World!"

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
        ustYields = fetchData.fetchSingleDayYield(datetime.today())#getUstYields(None) 
        #return Response(ustYields.to_json(orient ='index'), mimetype='application/json')
    elif request.method == "POST":
        received_date = request.get_json()
        input_date = received_date["yield date"]
        ustYields = fetchData.fetchSingleDayYield(datetime.strptime(input_date, "%Y-%m-%d"))#getUstYields(input_date)
        
    return Response(ustYields.to_json(orient ='index'), mimetype='application/json')

def getUstYields(yield_date):
    if not yield_date:
        t = datetime.today()
    else:
        t = datetime.strptime(yield_date, "%Y-%m-%d")
    
    ustYield = fetchData.fetchSingleDayYield(t)
        
    return ustYield.to_json(orient ='index')

if __name__ == "__main__":
    app.run("localhost", 6969)