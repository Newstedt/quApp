from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
import fetchData 
import numpy as np

class Bond:
    def __init__(self, cusip, issue_date, maturity, face, cpn_rate, cpn_freq):
        self.cusip = cusip
        self.maturity = maturity
        self.issue_date = issue_date
        self.face = face
        self.cpn_rate = cpn_rate
        self.cpn_freq = cpn_freq
        self.num_cfs = int(self.ttm()//(360/self.cpn_freq)) + 1
        
    def ttm(self):
        delta = self.maturity - max(date.today(), self.issue_date)
        return delta.days
    
    def theoPrice(self):
        return sum(self.cashflows().disc_cashflows.tolist())
    
    def cashflows(self):
        
        t = [x - max(date.today(), self.issue_date) for x in cfDates(self)]
        yields = fetchData.fetchSingleDayYield(date.today())
        yields.iloc[0]
        
        yields = fetchData.fetchSingleDayYield(date.today())
        tenors = yields.iloc[0].index.tolist()
        [convertCondition(x) for x in tenors]
        
        dates = [str(d) for d in cfDates(self)]
        days_to = [x.days for x in t]
        cashflows = cfAmounts(self) 
        discount_factors = cfDiscountFactors(self)
        disc_cashflows = discount_factors*np.array(cashflows)
        
        cf_df = pd.DataFrame(
            list(zip(dates, days_to, cashflows, disc_cashflows, discount_factors)),
            columns =['date', 'days_to', 'cashflow', 'disc_cashflows', 'discount_factor'])
        
        if cf_df.iloc[0].date == self.issue_date:
            return cf_df.iloc[1:]
        else:
            return cf_df
    
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
    cf_dates = [Bond.maturity - relativedelta(months=+12/Bond.cpn_freq*x) for x in cf_num]
    cf_dates.reverse()
    return cf_dates

def cfDiscountFactors(Bond):
    yields = fetchData.fetchSingleDayYield(date.today())
    tenor_days = [convertCondition(x) for x in yields.iloc[0].index.tolist()]
    yields_with_days = pd.DataFrame(
        list(zip([0]+tenor_days, [0]+yields.iloc[0].tolist())), 
        columns=['days','yield'])
    
    # Calculate number of days until each cashflow
    t = [x - max(date.today(), Bond.issue_date) for x in cfDates(Bond)]
    cf_days = [max(x.days,0) for x in t]
    
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