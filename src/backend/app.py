from flask import Flask;
from flask_cors import CORS
from flask import jsonify
from flask import request

import pandas as pd
import random

import yfinance as yf
import requests

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from html.parser import HTMLParser

import plotly.express as px
import chart_studio
import chart_studio.plotly as py2
import chart_studio.tools as tls

import os
import pprint

'''
HOW TO USE THIS SERVER SCRIPT:
`pip install flask` and `pip install flask_cors` before running this server.

Run the `export FLASK_ENV=development` terminal command once before any subsequent `flask run` commands.
'''

### Firebase setup
# Fetch the service account key JSON file contents
cred = credentials.Certificate('../../apex-pies.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://apex-pies-default-rtdb.firebaseio.com'
})

def publishPieToDB(age, risk, sector, userId):
  stocksDict=createStocksDict()
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

'''
Iterates through the stocks in stocks.csv and creates a nested dictionary
where the outer dictionary's keys are Sectors and its values are inner dictionaries.
The inner dictionary keys are Stock Tickers, and the values are all relevant data about
that stock. Right now, we only store the Beta of that Stock, but this can be expanded in
the future.
'''
def createStocksDict():
  df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../../resources/stocks.csv"))
  stocksDict = {}
  for x in df.index:
    sector = df["Sector"][x]
    ticker = df["Ticker"][x]
    beta = df["Beta"][x]

    # Initialize a new dictionary for a new sector to store that sector's stock information
    if sector not in stocksDict.keys():
      stocksDict[sector] = {}
    
    # Store the beta of this stock.
    # We can expand the info stored beyond just beta in the future!
    stocksDict[sector][ticker] = beta    

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

  # This map determines what data is available to be shown in the hovertext of each slice
  df = pd.DataFrame({"Ticker": tickers_list, 
                    "Percentage": vals, 
                    "Sector": sectors_list, 
                    "Beta": beta_list
                    })

  fig = px.pie(df,values="Percentage", names="Ticker", hover_data=["Sector", "Beta"])

  fig.update_traces(hovertemplate='Ticker: %{label} <br> Percentage: %{value}% <br> Sector: %{customdata[0][0]} <br> Beta: %{customdata[0][1]}')

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
    app.logger.info("Front-End Request: Age {age} Risk {risk} Sector {sector} UserId {userId}".format(age=age, risk=risk, sector=sector, userId=userId))

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
Pie-Making Logic
'''

def makePie(userAge, userRiskTolerance, userSectorOfInterest, stocksDict):
  targetPortfolioBeta = calculateTargetPortfolioBeta(userAge, userRiskTolerance)

  app.logger.info("Targeted Portfolio Beta: " + str(targetPortfolioBeta))

  ### Now that we have finalized a target beta for the portfolio,
  ### we can start the stock-picking algorithm that tries to balance
  ### the final portfolio to meet the target portfolio beta.

  # A list of dictionaries that describes the final overall Pie.
  # Each dictionary is information about one stock chosen for the Pie.
  pieDict = []

  # Only keeps track of the chosen stock tickers for the Pie in the order that they were selected.
  stocks=[]
  # Only keeps track of the betas of the chosen stocks for the Pie in the order that they were selected.
  betas = []

  # Choose a first stock for the portfolio that has a beta close to the target portfolio beta
  # to assist the beta balancing algorithm.
  # Choose the first stock from the user's selected Sector of Interest
  firstStockTicker = chooseFirstStock(userSectorOfInterest, targetPortfolioBeta, stocksDict)
  # Fetch the beta for the first chosen stock
  firstStockBeta = stocksDict[userSectorOfInterest][firstStockTicker]
  # Fetch other important public information on the first chosen stock
  # firstStockCompanyName = fetchYFinanceInfo(firstStockTicker)

  # Add the first chosen stock to the portfolio
  pieDict.append({"Ticker" : firstStockTicker , 
                  "Percentage" : 0.05, 
                  "Sector" : userSectorOfInterest, 
                  "Beta" : firstStockBeta})
  stocks.append(firstStockTicker)
  betas.append(firstStockBeta)

  # If the first chosen stock's beta is less than the target portfolio beta, then the next chosen stock
  # should raise the beta. Otherwise, the next chosen stock should reduce the beta.
  raiseBeta = firstStockBeta < targetPortfolioBeta

  # Choose the remaining stocks using the `raiseBeta` from the first chosen stock as a starting point.
  sectors = ["Tech", "Health", "Banking", "Energy"]
  for sector in sectors:
    # If we are picking stocks for the user's selected Sector of Interest, then
    # pick 10 stocks in that sector. Otherwise, pick only 3 stocks for each of the remaining sectors.
    # We have already picked the first stock in the portfolio from the user's selected Sector of Interest.
    # Therefore, the final portfolio will have 11 stocks from the user's selected Sector after we pick 10
    # more stocks from that Sector. The final portfolio will also have 9 stocks combined from the other 3
    # sectors because we pick 3 stocks in each. In total, there will be 20 stocks in the portfolio with
    # equal 5% weightage given to each.
    if (sector == userSectorOfInterest):
      numberOfStocksToPick = 10
    else:
      numberOfStocksToPick = 3
    
    for _ in range(numberOfStocksToPick):
      chosenStockTickerName, chosenStockBeta = chooseStock(sector, targetPortfolioBeta, raiseBeta, stocksDict)

      # Fetch other important public information on the chosen stock
      # app.logger.info("Fetching AlphaVantage for {ticker} ...".format(ticker=chosenStockTickerName))
      # chosenStockCompanyName = fetchFinancialInfo(chosenStockTickerName)
      # app.logger.info("Full Company Name of {ticker} is {name} ...".format(ticker=chosenStockTickerName, name=chosenStockCompanyName))

      # Add the chosen stock to the portfolio
      pieDict.append({"Ticker" : chosenStockTickerName , 
                      "Percentage" : 0.05, 
                      "Sector" : sector , 
                      "Beta" : chosenStockBeta})
      stocks.append(chosenStockTickerName)
      betas.append(chosenStockBeta)

      # Re-calculate the new average beta of the portfolio
      newPortfolioBeta = findAvgBeta(betas)

      # Re-evaluate whether the next chosen stock should raise or reduce the portfolio's beta
      raiseBeta = newPortfolioBeta < targetPortfolioBeta
      
  return pieDict, stocks, betas

def fetchFinancialInfo(ticker):
  ### Yfinance Approach:
  # yfTicker = yf.Ticker(ticker)
  # info_dict = yfTicker.info
  # companyName = info_dict['shortName']
  url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey=9K66FLMPJBSMC5N6'.format(ticker=ticker)
  r = requests.get(url)
  data = r.json()
  companyName = data['Name']

  return companyName

def calculateTargetPortfolioBeta(userAge, userRiskTolerance):
  # The Keys are the possible Risk Tolerance levels (1-10) from the user.
  # The Values are baseline betas for a portfolio made with the key's Risk Tolerance level.
  # TODO: May need to consider storing this in the Firebase DB, or at least as a global variable.
  riskToleranceBetaDict = {1: 0.7, 2: 0.75, 3: 0.8, 4: 0.9, 5: 1.0, 6: 1.05, 7: 1.1, 8: 1.2, 9: 1.25, 10: 1.35}

  # Fetch the baseline portfolio beta for the current customer based on their selected Risk Tolerance level.
  riskToleranceBaselineBeta = riskToleranceBetaDict[userRiskTolerance]

  # Calculate a cumulative portfolio beta for the current customer using a weighted
  # average between the beta associated with the customer's age and the beta associated
  # with the customer's selected Risk Tolerance.
  # 
  # The baseline beta associated with age is larger for younger customers, and it steadily
  # decreases as the customer age increases. This is because younger customers have more time
  # in their life to earn income and offset any losses in the market, so they can afford to be
  # more risky.
  # 
  # The baseline beta associated with the customer's selected Risk Tolerance was calculated above.
  # 
  # Younger customers have more weight given towards their selected Risk Tolerance than the beta
  # associated with their age. This allows younger customers to have more control over the riskiness
  # of their portfolio. Older customers have more weight given towards the baseline beta for their age.
  # Since the baseline beta for older customers is low, they don't have the freedom to create riskier 
  # portfolios.
  # 
  # TODO: This goes against Benjamin Graham's philosophy that the amount of risk in your portfolio should be 
  # determined not by age, but rather by how much effort one is willing to put into the management of
  # their portfolio.
  if (userAge >= 18 and userAge <= 25):
    ageRisk = 1.25
    return (0.4 * ageRisk) + (0.6 * riskToleranceBaselineBeta)
  elif (userAge >= 26 and userAge <= 40):
    ageRisk = 1.1
    return (0.45 * ageRisk) + (0.55 * riskToleranceBaselineBeta)
  elif (userAge >= 41 and userAge <= 50):
    ageRisk = 1.0
    return (0.5 * ageRisk) + (0.5 * riskToleranceBaselineBeta)
  elif (userAge >= 51 and userAge <= 60):
    ageRisk = 0.9
    return (0.55 * ageRisk) + (0.45 * riskToleranceBaselineBeta)
  elif (userAge >= 61 and userAge <= 70):
    ageRisk = 0.75
    return (0.6 * ageRisk) + (0.4 * riskToleranceBaselineBeta)
  else:
    ageRisk = 0.7
    return (0.65 * ageRisk) + (0.35 * riskToleranceBaselineBeta)

# Picks a stock from the given sector that is within +/- 0.2 beta
# from the target portfolio beta to serve as a good starting point
# for the balancing algorithm.
def chooseFirstStock(sector, targetBeta, stocksDict):
  # Get only the stocks info for the given sector
  currStocksSectorDict = stocksDict[sector]

  # Populate a list of stocks in the given sector that have a beta
  # +/- 0.2 from the target portfolio beta.
  tickersWithCloserBetaList = []
  for currStockTicker in currStocksSectorDict.keys():
    currStockBeta = currStocksSectorDict[currStockTicker]
    if (currStockBeta >= (targetBeta - 0.2) and currStockBeta <= (targetBeta + 0.2)):
      tickersWithCloserBetaList.append(currStockTicker)

  # Pick a random stock from the list of stocks with a beta close to the target portfolio beta
  tickerName = tickersWithCloserBetaList[random.randint(1, len(tickersWithCloserBetaList) - 1)]

  return tickerName

# Picks a random stock in the given sector that has a beta higher than targetBeta
# when raiseBeta is True, and lower than targetBeta when raiseBeta is False.
def chooseStock(sector, targetBeta, raiseBeta, stocksDict):
  # Pick a random stock from the given sector
  currStockTickerName, currStockBeta = pickRandomStock(stocksDict, sector)

  if (raiseBeta):
    while(currStockBeta <= targetBeta):
      # Keep picking stocks until we find one that is above the target beta.
      currStockTickerName, currStockBeta = pickRandomStock(stocksDict, sector)
  else:
    while(currStockBeta >= targetBeta):
      # Keep picking stocks until we find one that is below the target beta.
      currStockTickerName, currStockBeta = pickRandomStock(stocksDict, sector)

  return currStockTickerName, currStockBeta

# Picks a random stock in the given sector.
def pickRandomStock(stocksDict, sector):
  sectorStocksList = list(stocksDict[sector].keys())
  numberOfStocksInSector = len(sectorStocksList)
  randomStockIndex = random.randint(1, numberOfStocksInSector)
  
  randomStockTickerName = sectorStocksList[randomStockIndex]
  randomStockBeta = stocksDict[sector][randomStockTickerName]

  return randomStockTickerName, randomStockBeta

def findAvgBeta(betas):  
  return sum(betas) / len(betas)