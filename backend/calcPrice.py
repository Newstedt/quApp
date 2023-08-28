import fetchData
import structures
from datetime import date

cusip_code = '912810TU2'
bond_ref = fetchData.fetchBondRefData(cusip_code)
test = structures.Bond(cusip_code, bond_ref['maturityDate'], 100, bond_ref['interestRate']/100, bond_ref['interestPaymentFrequency'])

print(test.theoPrice())

#print(structures.cfDiscountFactors(test))
