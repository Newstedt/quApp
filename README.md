# quApp

This is a simple application which can be used to analyse US Treasury Bonds.

## Description

The application uses information from:

- Nasdaq Data Link: US Treasury Yield Curves
- Treasurydirect: Reference data for US Treasury Bonds

It then has the ability to calculate a theoretical price/discounted fair value of bonds, given CUSIP as an input. As a sub-product of that, it can also provide a cashflow matrix (with discounted cashflows and discount factors) assuming continous discounting, as well as historical movements in the US Treasury Yield (tenor-by-tenor). Additionally, a simple web application can be launched to showcase some of the capabilities of the code.

## How to run locally
* Setup venv: `python3 -m venv .venv`
* Install libraries: `pip install -r requirements.txt`
* Run app.py (will launch on localhost:6969): `python /backend/app.py`
* (To use super-simple UI): `python -m http.server --bind 127.0.0.1 8000`

**Note**: For the application to work, you need to setup a personal API key to Nasdaq Data Link, and store it in `backend/quandlApiKey.txt` (gitignored). You can setup an account and create a key for **FREE** at https://www.nasdaq.com/nasdaq-data-link.

## Comming

Value at Risk calculator given historical movements in the yield curve tenors.

## Authors

Contributors names and contact info

Gustav Nystedt
[@linkedin](https://www.linkedin.com/in/gustavnystedt/)
