from flask import Flask;
from flask_cors import CORS
from flask import jsonify
from flask import request

import pandas as pd
import numpy as np
import logging
import random

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

####
# `pip install flask` and `pip install flask_cors` before running this server.
# Run `python app.py` to start the server. Don't use `flask run`!
####


#Firebase setup
# Fetch the service account key JSON file contents
cred = credentials.Certificate('./apex-pies.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://apex-pies-default-rtdb.firebaseio.com'
})

app = Flask(__name__)

# logging.basicConfig(level=logging.DEBUG)

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

def publishPieToDB(age, risk, sector, userId):
  stocksDict=createDict()
  pieDict, stocks=makePie(age, risk, sector, stocksDict)
  app.logger.error(pprint.pformat(pieDict))

  betas = findBetas(sector, stocks, stocksDict)

  # replace the child value with the userID
  ref = db.reference().child(userId)

  # replace the value for pie to the dictionary created
  ref.set({
    'pie': pieDict,
    'avgBeta' : findAvgBeta(betas)
  })


def makePie(age, risk, sector, stocksDict):
  pieDict = []
  stocks=[]

  # This is for the first stock
  firstStock = chooseFirstStock(sector, risk, stocksDict)
  firstStockBeta = stocksDict[sector][firstStock]
  if (firstStockBeta > risk):
    raiseBeta = False
  else:
    raiseBeta = True

  pieDict.append({"Ticker" : firstStock , "Percentage" : 0.20, "Sector" : sector })
  stocks.append(firstStock)

  # This is for the remainders stocks
  for x in range(4):
    if ((x + 1) % 2 == 1):
          tickerName = chooseStock(sector, risk, raiseBeta, stocksDict)
    else:
      tickerName = chooseStock(sector, risk, not (raiseBeta), stocksDict)

    stocks.append(tickerName)
    # if ticker was not already chosen 
    pieDict.append({"Ticker" : tickerName , "Percentage" : 0.20, "Sector" : sector })
  return pieDict, stocks


def findBetas(sector, stocks, stocksDict):
  betas=[]
  for ticker in stocks:
    betas.append(stocksDict[sector][ticker])

  return betas

def findAvgBeta(betas):
  return sum(betas) / len(betas)

def chooseFirstStock(sector, targetBeta, stocksDict):
  stockNumber = random.randint(1, 47)
  stocksList = list(stocksDict[sector].keys())
  tickerName = stocksList[stockNumber]
  beta = stocksDict[sector][tickerName]

  while (not ((beta >= targetBeta - 0.25) and (beta <= targetBeta + 0.25))):
    tickerName = chooseFirstStock(sector, targetBeta, stocksDict)
  
  return tickerName

def chooseStock(sector, targetBeta, raiseBeta, stocksDict):
  stockNumber = random.randint(1, 47)
  stocksList = list(stocksDict[sector].keys())
  tickerName = stocksList[stockNumber]
  beta = stocksDict[sector][tickerName]

  if (raiseBeta):
    if (beta > targetBeta):
      return tickerName
    else:
      tickerName = chooseStock(sector, targetBeta, raiseBeta, stocksDict)
  else:
    if (beta < targetBeta):
      return tickerName
    else:
      tickerName = chooseStock(sector, targetBeta, raiseBeta, stocksDict)

  return tickerName


@app.route('/', methods = ['GET', 'POST'])
def calculatePies():
  if request.method == 'POST':
    age = request.json['age']
    risk = request.json['risk']
    sector = request.json['sector']
    userId = request.json['userId']
    app.logger.error("Age {age} Risk {risk} Sector {sector} UserId {userId}".format(age=age, risk=risk, sector=sector, userId=userId))

    # TODO: Pie Calculation Algorithm goes here!
    publishPieToDB(age, risk, sector, userId)

    return jsonify(pieDict)
  elif request.method == 'GET':
    # Don't worry about this GET case. It's only here if we need it in the future.

    app.logger.info("GET message received")
    return jsonify("GET Reply Message")


@app.route('/fetchpies', methods = ['POST'])
def calculatePies():
  return jsonify({})


app.run(debug=True)