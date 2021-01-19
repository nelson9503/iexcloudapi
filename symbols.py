import requests
import json

def getSymbols(token: str) -> list:
    url = "https://cloud.iexapis.com/stable/ref-data/symbols?token={}".format(token)
    r = requests.get(url)
    result = json.loads(r.text)
    symbols = []
    for item in result:
        symbols.append(item["symbol"].replace(".", "-"))
    return symbols