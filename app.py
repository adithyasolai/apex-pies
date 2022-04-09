from flask import Flask;
from flask_cors import CORS
from flask import jsonify
from flask import request

import pandas as pd
import numpy as np
import logging
import random

####
# `pip install flask` and `pip install flask_cors` before running this server.
# Run `python app.py` to start the server. Don't use `flask run`!
####

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

CORS(app)

data = ""



import os
from prettyprinter import pprint

def createDict():
  df = pd.read_csv(os.path.join(os.path.dirname(__file__), "./resources/stocks.csv"))
  stocksDict = {}
  counter = 0
  for x in df.index:
    sector = df["Sector"][x]
    ticker = df["Ticker"][x]
    beta = df["Beta"][x]

    if sector in stocksDict.keys(): #if the sector already is a key
        stocksDict[sector][ticker] = beta
    else:
        stocksDict[sector] = {}

  return stocksDict


stocksDict=createDict()

stocks = []
mainSector = "Tech"
riskTolerance = 1.25


def makePie(age, risk, sector):
  pieDict = {}
  pieDict["pie"] = []

  for x in range(4):
    tickerName = chooseStock(sector)
    # if ticker was not already chosen 
    pieDict["pie"].append({"Ticker" : tickerName , "Percentage" : 0.20, "Sector" : sector })
  return pieDict

def chooseStock(sector):
  stockNumber = random.randint(0,49)
  stocksList = list(stocksDict[sector].keys())
  tickerName = stocksList[stockNumber]
  return tickerName


age = 19
risk = 10
sector = 'Tech'
pieDict=makePie(age, risk, sector)

pprint(pieDict)









@app.route('/', methods = ['GET', 'POST'])
def calculatePies():

  if request.method == 'POST':
    age = request.json['age']
    risk = request.json['risk']
    sector = request.json['sector']
    app.logger.info("Age {age} Risk {risk} Sector {sector}".format(age=age, risk=risk, sector=sector))

    # TODO: Pie Calculation Algorithm goes here!

    pieDict = makePie(age, risk, sector)

    return jsonify(pieDict)
  elif request.method == 'GET':
    # Don't worry about this GET case. It's only here if we need it in the future.

    app.logger.info("GET message received")
    return jsonify("GET Reply Message")

# if __name__ == '__main__':
#   app.run(debug=True)