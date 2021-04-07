## Project for Jigsaw Labs fall/spring 2020–2021

This project queries an external API via Flask, which then itself provides an _internal_ API that is in turn queried by Streamlit.

Read data from [Texas Mixed Beverage Gross Receipts](https://data.texas.gov/Government-and-Taxes/Mixed-Beverage-Gross-Receipts/naix-2893) [json API](https://data.texas.gov/resource/naix-2893.json) which shows liqour sales per venue/merchant. Sales are broken down by beer, wine, liquor, cover charges. Overlay this on a map of Texas. 

Pull from TX API:
- Location name
- Location zip
- Location city
– Liquor receipts
– Wine receipts
– Beer receipts
– Cover charge receipts

ZIPs and Cities are provided as in Excel and csv format [here](https://www.unitedstateszipcodes.org/tx/#zips-list). Additional per-zip information available [here](https://www.zip-codes.com/zip-code-api-register.asp). The acceptable cities column was hand-curated to remove multiple spellings of the same city---this may have been a mistake, we'll see once we start to process addresses. Decommmissioned ZIPs were removed. Acceptable cities and Primary cities were combined.



#### Tech used: 
- Python 
- Flask
- Streamlit

#### Stretch goals

Hope to eventually overlay one or more data streams from CDC or IRS, many of which are indexed by ZIP.

