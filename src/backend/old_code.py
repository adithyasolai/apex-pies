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