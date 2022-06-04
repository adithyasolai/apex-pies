import finnhub
import pprint
import pandas as pd
import time

# use 2 clients to double the effective rate limit
# Rate limit for one account: 60 API Calls / 1 Minute
finnhub_client = finnhub.Client(api_key="cacgc7qad3i0nrodd95g")
finnhub_client2 = finnhub.Client(api_key="cack85iad3i0nrodgf80")

us_stocks_dict_list = finnhub_client.stock_symbols('US')
time.sleep(1)

# this will store all the stock data we want, and will eventually be made into a Pandas pd
stock_data_as_dict = {"Ticker": [],
                      "Name": [],
                      "Market Cap": [],
                      "Sector": [],
                      "Beta": []
                     }

i = 0
for stock_dict in us_stocks_dict_list:
  print('Processing Stock #{i}...'.format(i=i))
  curr_stock_ticker = stock_dict['symbol']
  
  try:
    curr_stock_profile = finnhub_client.company_profile2(symbol=curr_stock_ticker)
    curr_stock_financials = finnhub_client2.company_basic_financials(symbol=curr_stock_ticker, metric='all')
  except Exception as e:
    continue

  # Make sure the needed data was returned by the API before logging this stock's data in our csv file
  if set(('name', 'finnhubIndustry', 'marketCapitalization')).issubset(curr_stock_profile.keys()) and \
     ('beta') in curr_stock_financials['metric'].keys(): # for some reason, I can't use subset approach if it's just 1 field
    curr_stock_name = curr_stock_profile['name']
    # Market Cap unit is $Millions!
    curr_stock_market_cap = curr_stock_profile['marketCapitalization']
    curr_stock_sector = curr_stock_profile['finnhubIndustry']
    curr_stock_beta = curr_stock_financials['metric']['beta']

    # Don't log stocks that don't have a sector label or beta
    if curr_stock_sector != 'N/A' and curr_stock_beta is not None:
      stock_data_as_dict['Ticker'].append(curr_stock_ticker)
      stock_data_as_dict['Name'].append(curr_stock_name)
      stock_data_as_dict['Market Cap'].append(curr_stock_market_cap)
      stock_data_as_dict['Sector'].append(curr_stock_sector)
      stock_data_as_dict['Beta'].append(curr_stock_beta)

      print(curr_stock_ticker)
      print(curr_stock_name)
      print(curr_stock_market_cap)
      print(curr_stock_sector)
      print(curr_stock_beta)

      print()

  i+=1
  time.sleep(1)

stock_data_as_df = pd.DataFrame(stock_data_as_dict)

stock_data_as_df.head()

stock_data_as_df.to_csv('./../../resources/stocks_from_script.csv')
