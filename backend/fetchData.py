 # %%
import pandas as pd
import quandl
from datetime import timedelta, datetime
import requests

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

def fetchBondRefData(cusip):
    response = requests.get(f'https://www.treasurydirect.gov/TA_WS/securities/search?cusip={cusip}&format=json')
    json_response = response.json()

    fields = ['maturityDate', 'interestRate', 'interestPaymentFrequency', 'minimumToIssue']
    
    ref_data = {key: json_response[0].get(key) for key in fields}
    if ref_data.get('interestPaymentFrequency') == 'Semi-Annual':
        ref_data.update(interestPaymentFrequency=2)
    elif ref_data.get('interestPaymentFrequency') == 'None':
        ref_data.update(interestPaymentFrequency=1)
    
    if not ref_data.get('interestRate'):
        ref_data.update(interestRate=0)

    ref_data['faceValue'] = ref_data.pop('minimumToIssue')
    ref_data.update(faceValue=float(ref_data.get('faceValue')))
    ref_data.update(interestRate=float(ref_data.get('interestRate')))
    ref_data.update(maturityDate=datetime.strptime(ref_data.get('maturityDate'), '%Y-%m-%dT%H:%M:%S').date()) 
    
    return ref_data
    