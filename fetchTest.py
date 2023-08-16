 
 # %%

import numpy as np
import pandas as pd
import quandl
import plotly.express as px 

def testQuandl():
    quandl.ApiConfig.api_key = '_sa9augz3njcPisZEsii'
    ustYield = quandl.get('USTREASURY/REALYIELD')
    fig=px.line(x=ustYield.columns.values.tolist(), y=ustYield.loc[ustYield.index == '2023-08-15'].values.flatten().tolist())
    fig.show()

def main():
    testQuandl()

if __name__ == "__main__":
    main()
# %%
