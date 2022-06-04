import pandas as pd
import os
import pprint
import random

def makePie(userAge, userRiskTolerance, userSectorOfInterest):
  targetPortfolioBeta = calculateTargetPortfolioBeta(userAge, userRiskTolerance)

  ### Now that we have finalized a target beta for the portfolio,
  ### we can start the stock-picking algorithm that tries to balance
  ### the final portfolio to meet the target portfolio beta.

  # Fetch stock data from csv
  stocksDataDf = pd.read_csv(os.path.join(os.path.dirname(__file__), "../../resources/stocks_from_script.csv"))

  # A df that describes the final overall Pie.
  # Each row is information about one stock chosen for the Pie.
  pieDf = pd.DataFrame(columns = stocksDataDf.columns)

  # Choose a first stock for the portfolio that has a beta close to the target portfolio beta
  # to assist the beta balancing algorithm.
  # Choose the first stock from the user's selected Sector of Interest
  firstStockData = pickFirstStock(userSectorOfInterest, targetPortfolioBeta, stocksDataDf)

  # Add the first chosen stock to the portfolio
  pieDf = pieDf.append(firstStockData)

  # fetch the beta of the first stock
  firstStockBeta = firstStockData['Beta']

  # If the first chosen stock's beta is less than the target portfolio beta, then the next chosen stock
  # should raise the beta. Otherwise, the next chosen stock should reduce the beta.
  raiseBeta = firstStockBeta < targetPortfolioBeta

  # Choose the remaining stocks using the `raiseBeta` from the first chosen stock as a starting point.
  # The space at the end of "Energy " IS REQUIRED BECAUSE OF THE DATA FORMAT
  # TODO: Remove this extra space in the df cleaning or in the csv data itself. (probably better to clean the df)
  sectors = ["Technology", "Health Care", "Banking", "Energy "]
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
      chosenStockData = pickRandomStock(sector, targetPortfolioBeta, raiseBeta, stocksDataDf)

      # Add the chosen stock to the portfolio
      pieDf = pieDf.append(chosenStockData)

      # Re-calculate the new average beta of the portfolio
      newPortfolioBeta = pieDf['Beta'].mean()

      # Re-evaluate whether the next chosen stock should raise or reduce the portfolio's beta
      raiseBeta = newPortfolioBeta < targetPortfolioBeta
      
  return pieDf

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
def pickFirstStock(sector, targetBeta, stocksDataDf):
  # Get only the stocks info for the given sector
  currSectorStocksDataDf = stocksDataDf.loc[stocksDataDf['Sector'] == sector]

  # Filter down to stocks that have a beta that is within +/- 0.2 of the target portfolio beta
  closeBetaStocksDataDf = currSectorStocksDataDf.loc[(currSectorStocksDataDf['Beta'] >= (targetBeta - 0.2)) & (currSectorStocksDataDf['Beta'] <= (targetBeta + 0.2))]

  # Pick a random stock from the list of stocks with a beta close to the target portfolio beta
  randomStockIndex = random.randint(0, len(closeBetaStocksDataDf.index) - 1)
  chosenStockData = closeBetaStocksDataDf.iloc[randomStockIndex]

  # This data is in the form of a pd.Series
  return chosenStockData

# Picks a random stock in the given sector that has a beta higher than targetBeta when raiseBeta is True, 
# and lower than targetBeta when raiseBeta is False.
def pickRandomStock(sector, targetBeta, raiseBeta, stocksDataDf):
  print(sector)
  print(targetBeta)
  print(raiseBeta)
  print()

  # Get only the stocks info for the given sector
  selectedSectorStocksDataDf = stocksDataDf.loc[stocksDataDf['Sector'] == sector]

  # if raiseBeta is True, filter down to only stocks that have a beta > targetBeta
  # if raiseBeta is False, filter down to only stocks that have a beta <= targetBeta
  if raiseBeta:
    correctBetaRangeDf = selectedSectorStocksDataDf.loc[selectedSectorStocksDataDf['Beta'] > targetBeta]
  else:
    correctBetaRangeDf = selectedSectorStocksDataDf.loc[selectedSectorStocksDataDf['Beta'] <= targetBeta]

  # Pick a random stock from the list of stocks within the right sector and the right beta range
  randomStockIndex = random.randint(0, len(correctBetaRangeDf.index) - 1)
  chosenStockData = correctBetaRangeDf.iloc[randomStockIndex]

  # This data is in the form of a pd.Series
  return chosenStockData