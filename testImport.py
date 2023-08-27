import backend.fetchData as fetchData
from datetime import date

yields = fetchData.fetchSingleDayYield(date.today())
print(yields.head(10))



