import finnhub
import pprint
import time

finnhub_client = finnhub.Client(api_key="cacgc7qad3i0nrodd95g")

us_stocks_dict_list = finnhub_client.stock_symbols('US')

for stock_dict in us_stocks_dict_list[0:60]:
  current_ticker = stock_dict['symbol']
  print(current_ticker)

  curr_stock_profile = finnhub_client.company_profile2(symbol=current_ticker)

  if len(curr_stock_profile) != 0:
    # print(pprint.pformat(curr_stock_profile))

    print(curr_stock_profile['name'])
    print(curr_stock_profile['finnhubIndustry'])

    print()

  time.sleep(0.25)

  
