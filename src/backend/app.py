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

import time

'''
`pip install flask` and `pip install flask_cors` before running this server.

Run the `export FLASK_ENV=development` terminal command once before any subsequent `flask run` commands.
####
'''

#Firebase setup
# Fetch the service account key JSON file contents
cred = credentials.Certificate('../../apex-pies.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://apex-pies-default-rtdb.firebaseio.com'
})

import os
import pprint

def publishPieToDB(age, risk, sector, userId):
  stocksDict=createDict()
  pieDict, stocks, betas = makePie(age, risk, sector, stocksDict)
  app.logger.info("New Dict: \n" + pprint.pformat(pieDict))

  # replace the child value with the userID
  ref = db.reference().child(userId)

  # replace the value for pie to the dictionary created

  vizLink = makeViz(userId, pieDict)
  app.logger.info(pprint.pformat("New Viz Link: \n" + vizLink))

  iframe=tls.get_embed(vizLink)
  app.logger.info(pprint.pformat("New iFrame HTML: \n" + iframe))

  ref.set({
    'pie': pieDict,
    'avgBeta' : findAvgBeta(betas),
    'vizLink': vizLink,
    'iframe': iframe
  })

  app.logger.info("Published data to Firebase DB...")

def createDict():
  df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../../resources/stocks.csv"))
  stocksDict = {}
  for x in df.index:
    sector = df["Sector"][x]
    ticker = df["Ticker"][x]
    beta = df["Beta"][x]

    if sector in stocksDict.keys(): #if the sector already is a key
        stocksDict[sector][ticker] = beta
    else:
        stocksDict[sector] = {}

  return stocksDict

def makeViz(userID, pieDict):
  username = 'adithyasolai'
  api_key = 'TibH1jVTDgFFrOA1bbE6'

  tickers_list = []
  sectors_list = []
  beta_list = []
  for pie in pieDict:
      tickers_list.append(pie['Ticker'])
      sectors_list.append(pie['Sector'])
      beta_list.append(pie['Beta'])

  # Just giving equal % weightage to each slice of the pie
  vals = [0.0] * len(tickers_list)
  for i in range(len(tickers_list)):
      vals[i] = 100/len(tickers_list)

  # This map determines what is shown in the hovertext of each slice
  df = pd.DataFrame({"Ticker": tickers_list, "Percentage": vals, "Sector": sectors_list, "Beta": beta_list})

  fig = px.pie(df,values="Percentage", names="Ticker", hover_data=["Sector", "Beta"])

  fig.update_traces(hovertemplate='Ticker: %{label} <br> Percentage: %{value} <br> Sector: %{customdata[0][0]} <br> Beta: %{customdata[0][1]}')

  chart_studio.tools.set_credentials_file(username = username, api_key = api_key)
  fileName = str(userID) + "-viz"
  vizLink = py2.plot(fig, filename = fileName, auto_open = False)
  
  return vizLink


'''
GET/POST Handlers that get called by front-end.
'''

app = Flask(__name__)
CORS(app)

@app.route('/', methods = ['GET', 'POST'])
def calculatePies():
  if request.method == 'POST':
    app.logger.info("Starting / POST Run...")
    age = int(request.json['age'])
    risk = int(request.json['risk'])
    sector = request.json['sector']
    userId = request.json['userId']
    #app.logger.error("Age {age} Risk {risk} Sector {sector} UserId {userId}".format(age=age, risk=risk, sector=sector, userId=userId))

    # TODO: Pie Calculation Algorithm goes here!
    publishPieToDB(age, risk, sector, userId)

    app.logger.info("Finished / POST Run...")

    return jsonify("POST Reply Message")
  elif request.method == 'GET':
    # Don't worry about this GET case. It's only here if we need it in the future.

    app.logger.info("GET message received")
    return jsonify("GET Reply Message")


@app.route('/fetchpies', methods = ['POST'])
def fetchPies():
  app.logger.info("Starting /fetchpies POST Run...")

  userId = request.json['userId']
  result = db.reference().child(userId)

  resultDict = result.get()

  # Append Plotly credentials to API
  resultDict['username'] = "adithyasolai"
  resultDict['apiKey'] = "TibH1jVTDgFFrOA1bbE6"

  app.logger.info("Result Dict Sent to User: \n" + pprint.pformat(resultDict))

  return jsonify(resultDict)


'''
Uncomment the line below to manually allow Debug Mode when 
starting this Flask server. If uncommented, Debug Mode will
only be activated if the `python app.py` terminal command is used.

Alternatively, keep this line of code commented and just run the
`export FLASK_ENV=development` terminal command once before 
any subsequent `flask run` commands.
'''
# app.run(debug=True)


'''
Pie-Making Logic put here for organization
'''

def makePie(age, userRisk, sector, stocksDict):
  pieDict = []
  stocks=[]
  betas = []
  riskDict = {1: 0.7, 2: 0.75, 3: 0.8, 4: 0.9, 5: 1.0, 6: 1.05, 7: 1.1, 8: 1.2, 9: 1.25, 10: 1.35}
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

  pieDict.append({"Ticker" : firstStock , "Percentage" : 0.05, "Sector" : sector, "Beta" : firstStockBeta })
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
      pieDict.append({"Ticker" : tickerName , "Percentage" : 0.05, "Sector" : sec , "Beta" : stocksDict[sec][tickerName]})
    
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