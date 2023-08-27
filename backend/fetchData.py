 # %%
import pandas as pd
import quandl
from datetime import timedelta

def fetchHistYield(start_date, end_date):
    with open('backend/quandlApiKey.txt', 'r') as f:
        quandlKey = f.readline()
        f.close()
    quandl.ApiConfig.api_key = quandlKey
    ustYield = quandl.get('USTREASURY/YIELD', start_date=start_date, end_date=end_date)
    
    return ustYield

def fetchSingleDayYield(date):
    with open('backend/quandlApiKey.txt', 'r') as f:
        quandlKey = f.readline()
        f.close()
    quandl.ApiConfig.api_key = quandlKey
    ustYield = pd.DataFrame()
    while ustYield.empty:
        ustYield = quandl.get('USTREASURY/YIELD', start_date=date, end_date=date)
        date = date - timedelta(days=1)
    return ustYield

def histReturn(start_date, end_date):
    histYield = fetchHistYield(start_date, end_date)
    histReturns = (histYield - histYield.shift(1))/histYield.shift(1)
    #histReturns.iloc[1:].to_csv('resources/histUstReturns.csv', mode='w+')
    return histReturns.iloc[1:]

