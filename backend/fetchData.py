import pandas as pd
import quandl
from datetime import timedelta, datetime
import requests
from bs4 import BeautifulSoup
import json

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

    fields = ['issueDate','maturityDate', 'interestRate', 'interestPaymentFrequency', 'minimumToIssue', 'frnIndexDeterminationRate', 'spread']
    
    ref_data = {key: json_response[0].get(key) for key in fields}
    if ref_data.get('interestPaymentFrequency') == 'Semi-Annual':
        ref_data.update(interestPaymentFrequency=2)
    elif ref_data.get('interestPaymentFrequency') == 'None': 
        ref_data.update(interestPaymentFrequency=1)
    elif ref_data.get('interestPaymentFrequency') == 'Quarterly':
        ref_data.update(interestPaymentFrequency=4)
    
    if not ref_data.get('interestRate') and ref_data.get('interestPaymentFrequency') == 1:
        ref_data.update(interestRate=0)
    elif not ref_data.get('interestRate') and ref_data.get('interestPaymentFrequency') == 4:
        ref_data.update(interestRate=float(ref_data.get('frnIndexDeterminationRate')) + float(ref_data.get('spread'))) #in case quarterly with no interest QUARTERLY should use: FrnIndexDeterminationRate + spread

    ref_data['faceValue'] = ref_data.pop('minimumToIssue')
    ref_data.update(faceValue=float(ref_data.get('faceValue')))
    ref_data.update(interestRate=float(ref_data.get('interestRate')))
    ref_data.update(maturityDate=datetime.strptime(ref_data.get('maturityDate'), '%Y-%m-%dT%H:%M:%S').date()) 
    ref_data.update(issueDate=datetime.strptime(ref_data.get('issueDate'), '%Y-%m-%dT%H:%M:%S').date())
    
    return ref_data

def getCusipList():
    url = requests.get("https://treasurydirect.gov/TA_WS/securities/auctioned").content

    soup = BeautifulSoup(url, 'html.parser')
    data = json.loads(str(soup.contents[0].string))

    cusip_list = [x['cusip'] for x in data]
    return cusip_list