import time
import unittest
import time
import requests
import okx.MarketData as MarketData

timestamp = int(time.time() * 1000)

url_bin = "https://api.binance.com/api/v3/ticker/price"
url_bit = "https://api-testnet.bybit.com/v5/market/tickers?category=spot"

def get_price(url):
    response = requests.get(url)
    data = response.json()
    return data

tickers_bin = []
data_bin = get_price(url_bin)
for d in data_bin:
    if d['symbol'][4:] == 'USDT':
        tickers_bin.append(d)

tickers_bit = []
data_bit = get_price(url_bit)
for data in data_bit:
    for d in data_bit['result']['list']:
        if d['symbol'][4:] == 'USDT':
            tickers_bit.append(d)

flag = "0"  # Production trading:0 , demo trading:1
marketDataAPI = MarketData.MarketAPI(flag=flag)
# Retrieve the latest price snapshot, best bid/ask price, and trading volume in the last 24 hours
result = marketDataAPI.get_tickers(
    instType="SPOT"
)

tickers_okx = []
data_okx = result
for data in data_okx['data']:
    if data['instId'][4:] == 'USDT':
          tickers_okx.append(data)

def get_whitelisted_token_prices():
    tickers_1inch = []
    url = "https://api.1inch.dev/price/v1.1/1"
    response = requests.get(url, headers={'Authorization': f'UNfmcKAyoQSZ3iEr27o4SZbr2xx0j6Su'})
    if response.status_code == 200:
        prices = response.json()
        print("Prices for whitelisted tokens:")
        for token_address, price in prices.items():
            print(f"{token_address}: {price}")
    else:
        print("Failed to fetch token prices.")
    for data in prices:
        tickers_1inch.append(data)
    print(tickers_1inch)
    return tickers_1inch

tickers_1inch = get_whitelisted_token_prices()


