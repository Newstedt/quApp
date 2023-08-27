import fetchData
import structures
from datetime import date


test = structures.Bond('1235677777', date(2028, 6, 10), 100, 0.05, 2)
#df = test.cashflows()
#print(df.head(10))

print(structures.cfDiscountFactors(test).head(10))
