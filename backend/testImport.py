import calcPrice


theoPrice, bondCashflows = calcPrice.theoPriceFromCusip('91282CHW4')
print(bondCashflows[1].to_json(orient ='index'))