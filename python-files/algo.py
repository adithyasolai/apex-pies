import pandas as pd
import random
import os
from prettyprinter import pprint

df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../resources/stocks.csv"))

stocksDict = {}


def createDict():    
    counter = 0
    for x in df.index:
        sector = df["Sector"][x]
        ticker = df["Ticker"][x]
        beta = df["Beta"][x]

        if sector in stocksDict.keys(): #if the sector already is a key
            stocksDict[sector][ticker] = beta
        else:
            stocksDict[sector] = {}


createDict()

pprint (stocksDict)
stocks = []
mainSector = "Tech"
riskTolerance = 1.25

# def pickStocks(mainSector, riskTolerance):

#     #Initialization
#     createDict()
#     mainDict = {}
#     if (mainSector == "Tech"):
#         mainDict = techDict
#     elif (mainSector == "Health"):
#         mainDict = healthDict
#     elif (mainSector == "Energy"):
#         mainDict = energyDict
#     elif (mainSector == "Banking"):
#         mainDict = bankingDict
#     elif (mainSector == "Crypto"):
#         mainDict = cryptoDict

#     # Target beta is the risk tolerance that they provide
#     targetBeta = riskTolerance
#     totalBeta = 0

#     findFirstStock(mainDict, riskTolerance)



# def findStock(mainDict, riskTolerance):
#     stock = mainDict["Tech" + str(random.randint(1, 50))]
#     for key, value in firstStock.items():
#         ticker = key
#         beta = value
    
#     stocks.append(ticker)
#     totalBeta = totalBeta + beta

#     if (beta > riskTolerance):
#         raiseBeta = False
#     else: 
#         raiseBeta = True
    
#     pickRemainderStocks(ticker, raiseBeta)

# pickStocks("Tech", 1.25)


# def pickRemainderStocks(ticker, betaRaise):
#     return 0
#     # if (betaRaise == True):


