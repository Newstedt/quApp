from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
import fetchData
import numpy as np

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
    
    def theoPrice(self):
        return sum(self.cashflows().disc_cashflows.tolist())
    
    def cashflows(self):
        
        #currently only supporting SEMI_ANNUAL coupon frequency
        if self.cpn_rate == 0:
            return pd.DataFrame(
            list(zip([0], [0], [0], [0], [0])),
            columns =['date', 'days_to', 'cashflow', 'disc_cashflows', 'discount_factor'])
            
        t = [x - date.today() for x in cfDates(self)]
        yields = fetchData.fetchSingleDayYield(date.today())
        yields.iloc[0]
        
        yields = fetchData.fetchSingleDayYield(date.today())
        tenors = yields.iloc[0].index.tolist()
        [convertCondition(x) for x in tenors]
        
        dates = cfDates(self) 
        days_to = [x.days for x in t]
        cashflows = cfAmounts(self) 
        discount_factors = cfDiscountFactors(self)
        disc_cashflows = discount_factors*np.array(cashflows)
        
        return pd.DataFrame(
            list(zip(dates, days_to, cashflows, disc_cashflows, discount_factors)),
            columns =['date', 'days_to', 'cashflow', 'disc_cashflows', 'discount_factor'])
    
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
        list(zip(tenor_days, yields.iloc[0].tolist())), 
        columns=['days','yield'])
    t = [x - date.today() for x in cfDates(Bond)]
    cf_days = [x.days for x in t]
    
    r = [interpolateYield(x,yields_with_days)/100 for x in cf_days]
    d = np.exp(-np.array(r)*np.array(cf_days)/360)
    return d
    
def interpolateYield(x, yields_with_days):
    x_values = yields_with_days['days'].tolist()
    y_values = yields_with_days['yield'].tolist()
    # Check if x is outside the range of x_values
    if x < x_values[0] or x > x_values[-1]:
        raise ValueError("Input x is outside the range of x_values")

    # Find the two closest x values in x_values
    idx_left = np.searchsorted(x_values, x, side='right') - 1
    idx_right = idx_left + 1

    # Perform linear interpolation
    x_left, x_right = x_values[idx_left], x_values[idx_right]
    y_left, y_right = y_values[idx_left], y_values[idx_right]

    y_interpolated = y_left + (x - x_left) * (y_right - y_left) / (x_right - x_left)

    return y_interpolated
 
def convertCondition(tenor):
    num = [int(x) for x in tenor.split() if x.isdigit()][0]
    if 'MO' in tenor:
        days = num*30
    else:
        days = num*360
    return days