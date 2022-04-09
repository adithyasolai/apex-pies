import pandas as pd
import random

df = pd.read_csv('../resources/stocks.csv')

techDict = {}
healthDict = {}
energyDict = {}
bankingDict = {}
cryptoDict = {}


def createDict():    
    counter = 0
    for x in df.index:
        techDict[str(df['Sector'][x]) + str(x + 1)] = {df['Ticker'][x]:df['Beta'][x]}
        healthDict[str(df['Sector'][x + 51]) + str(x + 51)] = {df['Ticker'][x + 51]: df['Beta'][x + 51]}
        energyDict[str(df['Sector'][x + 51 * 2]) + str(x + 51 * 2)] = {df['Ticker'][x + 51 * 2] : df['Beta'][x + 51 * 2]}
        bankingDict[str(df['Sector'][x + 51 * 3]) + str(x + 51 * 3)] = {df['Ticker'][x + 51 * 3] : df['Beta'][x + 51 * 3]}
        cryptoDict[str(df['Sector'][x + 51 * 4]) + str(x + 51 * 4)] = {df['Ticker'][x + 51 * 4] : df['Beta'][x + 51 * 4]}
        counter += 1

        if (counter == 51):
            break



stocks = []
mainSector = "Tech"
riskTolerance = 1.25

def pickStocks(mainSector, riskTolerance):

    #Initialization
    createDict()
    mainDict = {}
    if (mainSector == "Tech"):
        mainDict = techDict
    elif (mainSector == "Health"):
        mainDict = healthDict
    elif (mainSector == "Energy"):
        mainDict = energyDict
    elif (mainSector == "Banking"):
        mainDict = bankingDict
    elif (mainSector == "Crypto"):
        mainDict = cryptoDict

    # Target beta is the risk tolerance that they provide
    targetBeta = riskTolerance
    totalBeta = 0

    findFirstStock(mainDict, riskTolerance)



def findStock(mainDict, riskTolerance):
    stock = mainDict["Tech" + str(random.randint(1, 50))]
    for key, value in firstStock.items():
        ticker = key
        beta = value
    
    stocks.append(ticker)
    totalBeta = totalBeta + beta

    if (beta > riskTolerance):
        raiseBeta = False
    else: 
        raiseBeta = True
    
    pickRemainderStocks(ticker, raiseBeta)

pickStocks("Tech", 1.25)


def pickRemainderStocks(ticker, betaRaise):

    if (betaRaise == True):


