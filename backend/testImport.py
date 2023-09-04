import calcPrice


theoPrice, bondCashflows = calcPrice.theoPriceFromCusip('91282CHW4')
print(bondCashflows.to_json(orient ='index'))