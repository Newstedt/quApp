import fetchData
import structures

def theoPriceFromCusip(cusip):
    bond_ref = fetchData.fetchBondRefData(cusip)
    bond_struct = structures.Bond(
        cusip, 
        bond_ref['issueDate'], 
        bond_ref['maturityDate'], 
        100, #default to 100 for now
        bond_ref['interestRate']/100, 
        bond_ref['interestPaymentFrequency'])
    
    cashflows = bond_struct.cashflows()
    theoPrice = sum(cashflows.disc_cashflows.tolist())
    return theoPrice, cashflows
