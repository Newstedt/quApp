 # %%

import numpy as np
import pandas as pd
import quandl
import plotly.express as px 

t = 1
def testQuandl():
    with open('quandlApiKey.txt', 'r') as f:
        quandlKey = f.readline()
        f.close()
    quandl.ApiConfig.api_key = quandlKey
    ustYield = quandl.get('USTREASURY/REALYIELD')
    fig=px.line(
        x=ustYield.columns.values.tolist(), 
        y=ustYield.loc[ustYield.index == '2023-08-15'].values.flatten().tolist())
    fig.show()

def main():
    testQuandl()

if __name__ == "__main__":
    main()

