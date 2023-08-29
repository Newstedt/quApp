import pandas as pd
technologies = {
    'Courses':["Spark","PySpark","Python","pandas","Hadoop"],
    'Fee' :[20000,25000,22000,24000,30000],
    'Duration':['30day','40days','35days','60days','55days'],
    'Discount':[1000,2300,2500,2000,3000]
              }


df = pd.DataFrame(technologies)
print(df.iloc[0].Courses)