import fetchData
import structures

#cusip = '91282CHS3'

def theoPriceFromCusip(cusip):
    bond_ref = fetchData.fetchBondRefData(cusip)
    bond_struct = structures.Bond(
        cusip_code, 
        bond_ref['issueDate'], 
        bond_ref['maturityDate'], 
        100, 
        bond_ref['interestRate']/100, 
        bond_ref['interestPaymentFrequency'])
    
    return bond_struct.theoPrice()
