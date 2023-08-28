import requests
import backend.fetchData as fd
from datetime import datetime
bond_ref = fd.fetchBondRefData('912810TP3')
print(bond_ref['maturityDate'])
