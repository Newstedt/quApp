from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
import fetchData

class Bond:
    def __init__(self, isin, maturity, face, cpn_rate, cpn_freq):
        self.isin = isin
        self.maturity = maturity
        self.face = face
        self.cpn_rate = cpn_rate
        self.cpn_freq = cpn_freq
        self.num_cfs = int(self.ttm()//(360/self.cpn_freq))
        
    def ttm(self):
        delta = self.maturity - date.today()
        return delta.days
    
    def cashflows(self):
        t = [x - date.today() for x in cfDates(self)]
        yields = fetchData.fetchSingleDayYield(date.today())
        yields.iloc[0]
        
        yields = fetchData.fetchSingleDayYield(date.today())
        tenors = yields.iloc[0].index.tolist()
        [convertCondition(x) for x in tenors]
        
        return pd.DataFrame(
            list(zip(cfDates(self), [x.days for x in t], cfAmounts(self))),  
            columns =['date', 'days_to', 'cashflow'])
    
    #def discountFactors(self):
        
        
class Curve:
    def __init__(self, issuer, yields):
        self.issuer = issuer
        self.yields = yields
    
    def getYieldByTenor(self, tenor):
        return self.yields[tenor]
       
def cfAmounts(Bond):
    cfs = [x * Bond.face*Bond.cpn_rate/Bond.cpn_freq for x in [1]*Bond.num_cfs]
    cfs[-1] = cfs[-1] + Bond.face
    return cfs

def cfDates(Bond):
    cf_num = list(range(0, int(Bond.num_cfs)))
    cf_dates = [Bond.maturity - relativedelta(months=+6*x) for x in cf_num]
    cf_dates.reverse()
    return cf_dates

def cfDiscountFactors(Bond):
    yields = fetchData.fetchSingleDayYield(date.today())
    tenor_days = [convertCondition(x) for x in yields.iloc[0].index.tolist()]
    yields_with_days = pd.DataFrame(
        list(zip(days_to_tenors, yields.iloc[0].tolist())), 
        columns=['days','yield'])
    t = [x - date.today() for x in cfDates(Bond)]
    # !!!!!!! CONTINUE HERE !!!!!!! 
    cf_days = [x.days for x in t]
    min(cf_days, key=lambda x:abs(x-myNumber))
    temp = [x-18 for x in tenor_days]
    #cf_yield = 
    cf_amounts = cfAmounts(Bond)
    
    
    
 
def convertCondition(tenor):
    num = [int(x) for x in tenor.split() if x.isdigit()][0]
    if 'MO' in tenor:
        days = num*30
    else:
        days = num*360
    return days