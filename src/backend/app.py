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
from html.parser import HTMLParser

import plotly.express as px
import plotly
from bs4 import BeautifulSoup
import chart_studio
import chart_studio.plotly as py2
import chart_studio.tools as tls



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

import os
import pprint

def publishPieToDB(age, risk, sector, userId):
  stocksDict=createDict()
  pieDict, stocks, betas = makePie(age, risk, sector, stocksDict)
  # app.logger.error(pprint.pformat(pieDict))

  # replace the child value with the userID
  ref = db.reference().child(userId)

  # replace the value for pie to the dictionary created
  # ref.set({
  #   'pie': pieDict,
  #   'avgBeta' : findAvgBeta(betas)
  # })

  
  # vizLink = makeViz(userId, pieDict)
  # app.logger.error(pprint.pformat(vizLink))

  # iframe=tls.get_embed(vizLink)
  # app.logger.error(pprint.pformat(iframe))


  ref.set({
    'pie': pieDict,
    'avgBeta' : findAvgBeta(betas),
    'vizLink': vizLink,
    'iframe': iframe
  })

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


def makePie(age, userRisk, sector, stocksDict):
  pieDict = []
  stocks=[]
  betas = []
  riskDict = {1: 0.7, 2: 0.75, 3: 0.8, 4: 0.9, 5: 1.0, 6: 1.05, 7: 1.1, 8: 1.2, 9:1.25, 10:1.35}
  riskBetaVal = riskDict[userRisk]

  if (age >= 18 and age <= 25):
    ageRisk = 1.25
    weightedRisk = (0.6 * ageRisk) + (0.4 * riskBetaVal)
  elif (age >= 26 and age <= 40):
    ageRisk = 1.1
    weightedRisk = (0.5 * ageRisk) + (0.5 * riskBetaVal)
  elif (age >= 41 and age <= 50):
    ageRisk = 1.0
    weightedRisk = (0.4 * ageRisk) + (0.6 * riskBetaVal)
  elif (age >= 51 and age <= 60):
    ageRisk = 0.9
    weightedRisk = (0.5 * ageRisk) + (0.5 * riskBetaVal)
  elif (age >= 61 and age <= 70):
    ageRisk = 0.75
    weightedRisk = (0.6 * ageRisk) + (0.4 * riskBetaVal)
  else:
    ageRisk = 0.7
    weightedRisk = (0.65 * ageRisk) + (0.35 * riskBetaVal)

  # This is for the first stock
  firstStock = chooseFirstStock(sector, weightedRisk, stocksDict)
  firstStockBeta = stocksDict[sector][firstStock]
  if (firstStockBeta > weightedRisk):
    raiseBeta = False
  else:
    raiseBeta = True

  pieDict.append({"Ticker" : firstStock , "Percentage" : 0.05, "Sector" : sector })
  stocks.append(firstStock)

  # This is for the remainders stocks
  sectors = ["Tech", "Health", "Banking", "Energy"]
  for sec in sectors:
    if (sec == sector):
      length = 11
    else:
      length = 3
    
    tempStocksList = []
    for x in range(length):
      if (length == 3):
        if ((x + 1) % 2 == 1):
            tickerName = chooseStock(sec, weightedRisk, raiseBeta, stocksDict)
      else:
        if ((x + 1) % 2 == 1):
              tickerName = chooseStock(sec, weightedRisk, raiseBeta, stocksDict)
        else:
          tickerName = chooseStock(sec, weightedRisk, not (raiseBeta), stocksDict)

      stocks.append(tickerName)
      tempStocksList.append(tickerName)
      # if ticker was not already chosen 
      pieDict.append({"Ticker" : tickerName , "Percentage" : 0.05, "Sector" : sec })
    
    betasAdd = findBetas(sec, tempStocksList, stocksDict)
    for val in betasAdd:
      betas.append(val)

  return pieDict, stocks, betas

def chooseFirstStock(sector, targetBeta, stocksDict):
  # stockNumber = random.randint(1, 47)
  stocksList = list(stocksDict[sector].keys())

  closerBetaList = []
  for ticker in stocksList:
    beta = stocksDict[sector][ticker]
    if (beta >= (targetBeta - 0.2) and (beta <= targetBeta + 0.2)):
      closerBetaList.append(ticker)
  
  tickerName = closerBetaList[random.randint(1, len(closerBetaList) - 1)]

  return tickerName

def chooseStock(sector, targetBeta, raiseBeta, stocksDict):
  listStocks = []
  cont = True
  if (raiseBeta):
    while(cont == True):
      stockNumber = random.randint(1, 47)
      stocksList = list(stocksDict[sector].keys())
      tickerName = stocksList[stockNumber]
      beta = stocksDict[sector][tickerName]
      if (beta > targetBeta):
        listStocks.append(tickerName)
        cont = False
  else:
    while(cont == True):
      stockNumber = random.randint(1, 47)
      stocksList = list(stocksDict[sector].keys())
      tickerName = stocksList[stockNumber]
      beta = stocksDict[sector][tickerName]
      if (beta < targetBeta):
        listStocks.append(tickerName)
        cont = False

  return tickerName

def findBetas(sector, stocks, stocksDict):
  betas=[]
  for ticker in stocks:
    betas.append(stocksDict[sector][ticker])

  return betas

def findAvgBeta(betas):
  
  return sum(betas) / len(betas)



def makeViz(userID, pieDict):
  username = 'bhuvan.jama'
  api_key = 'athHaKcHBgzSdbrNI8md'

  tickers = {}
  for dictionary in pieDict:
      tickers[dictionary['Ticker']] = "5.0%"

  tickers_list = list(tickers.keys())

  vals = [0.0] * len(tickers_list)
  for i in range(len(tickers_list)):
      vals[i] = 100/len(tickers_list)


  df = pd.DataFrame({"Ticker": tickers_list, "Percentages": vals})

  fig = px.pie(df,values="Percentages", names="Ticker")
  fig.show()      

  chart_studio.tools.set_credentials_file(username = username, api_key = api_key)
  fileName = str(userID) + "-viz"
  vizLink = py2.plot(fig, filename = fileName, auto_open = False)
  
  return vizLink


app = Flask(__name__)
CORS(app)

@app.route('/', methods = ['GET', 'POST'])
def calculatePies():
  if request.method == 'POST':
    age = int(request.json['age'])
    risk = int(request.json['risk'])
    sector = request.json['sector']
    userId = request.json['userId']
    #app.logger.error("Age {age} Risk {risk} Sector {sector} UserId {userId}".format(age=age, risk=risk, sector=sector, userId=userId))

    # TODO: Pie Calculation Algorithm goes here!
    publishPieToDB(age, risk, sector, userId)

    return jsonify("POST Reply Message")
  elif request.method == 'GET':
    # Don't worry about this GET case. It's only here if we need it in the future.

    app.logger.info("GET message received")
    return jsonify("GET Reply Message")


@app.route('/fetchpies', methods = ['POST'])
def fetchPies():
  userId = request.json['userId']
  result = db.reference().child(userId)

  resultDict = result.get()

  resultDict['username'] = "bhuvan.jama"
  resultDict['apiKey'] = "athHaKcHBgzSdbrNI8md"

  app.logger.error(type(resultDict))
  app.logger.error(pprint.pformat(resultDict))

  return jsonify(resultDict)
  # return jsonify(result)


app.run(debug=True)