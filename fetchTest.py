 # %%

import numpy as np
import pandas as pd
import quandl
import plotly.express as px 

t = 1
testitt = testQuandl()
def testQuandl():
    with open('backend/quandlApiKey.txt', 'r') as f:
        quandlKey = f.readline()
        f.close()
    quandl.ApiConfig.api_key = quandlKey
    ustYield = quandl.get('USTREASURY/REALYIELD')
    """fig=px.line(
        x=ustYield.columns.values.tolist(), 
        y=ustYield.loc[ustYield.index == '2023-08-15'].values.flatten().tolist())
    fig.show()"""
    return ustYield

def main():
    testit = testQuandl()

if __name__ == "__main__":
    main()


# %%
