import time
import unittest
import time
import requests
import okx.MarketData as MarketData
from python_1inch import OneInchExchange

timestamp = int(time.time() * 1000)

url_bin = "https://api.binance.com/api/v3/ticker/price"
url_bit = "https://api-testnet.bybit.com/v5/market/tickers?category=spot"

def get_price(url):
    response = requests.get(url)
    data = response.json()
    return data

# Получаем все символы и цены с BINANCE_________________________________________________________________________________
tickers_bin = []
data_bin = get_price(url_bin)
for d in data_bin:
    if d['symbol'][4:] == 'USDT':
        tickers_bin.append(d)

# Получаем все символы и цены с BYBIT___________________________________________________________________________________
tickers_bit = []
data_bit = get_price(url_bit)
for data in data_bit:
    for d in data_bit['result']['list']:
        if d['symbol'][4:] == 'USDT':
            tickers_bit.append(d)

# Получаем все символы и цены с OKX_____________________________________________________________________________________
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

# Получаем все адреса контрактов с 1inch________________________________________________________________________________
def get_whitelisted_token_prices():
    tickers_1inch = []
    url = "https://api.1inch.dev/price/v1.1/1"
    response = requests.get(url, headers={'Authorization': f'UNfmcKAyoQSZ3iEr27o4SZbr2xx0j6Su'})
    if response.status_code == 200:
        prices = response.json()
        print("Prices for whitelisted tokens:")
    else:
        print("Failed to fetch token prices.")
    for data in prices:
        tickers_1inch.append(data)
    return tickers_1inch

tickers_1inch = get_whitelisted_token_prices()

# Получаем все тикеры с адресами контрактов с Coingwcko_________________________________________________________________
def get_all_tickers():
    url = f'https://api.coingecko.com/api/v3/coins/list?include_platform=true'
    response = requests.get(url)
    data = response.json()
    return data
#     for d in data:
#         if 'ethereum' in d['platforms']:
#             if d['platforms']['ethereum'] == contract_adress:
#                 all_tickers.append(d['symbol'])

# Запрос адреса контракта для конкретной сети и запись инфо о символе и адресе в массив_________________________________
def get_contract_adress(sym, chain, array):
    for token in all_tickers:
        if sym == token["symbol"]:
            if chain in token['platforms']:
                contract_adress = token['platforms'][chain]
                crypto = {
                    'symbol': sym,
                    'contract_adress': contract_adress
                }
                array.append(crypto)
            else:
                continue

def get_requested_token_prices(tokens):
    url = "https://api.1inch.dev/price/v1.1/1"

    payload = {
        "tokens": tokens
    }

    response = requests.post(url)
    print(response)
    # , json=payload)
    # if response.status_code == 200:
    #     prices = response.json()
    #     print("Prices for requested tokens:")
    #     for token_address, price in prices.items():
    #         print(f"{token_address}: {price}")
    # else:
    #     print("Failed to fetch token prices.")

# Создаём массивы под каждую сеть_______________________________________________________________________________________
ethereum = []
zksync = []
arbitrum = []
binance = []
polygon = []
avalanche = []

ethereum_1inch = []

# Получаем все тикеры с адресами контрактов c Сoingwcko_________________________________________________________________
all_tickers = get_all_tickers()

# Получаем адреса контрактов по символам из массива_____________________________________________________________________
for d in tickers_bin:
    get_contract_adress(d['symbol'][:-4].lower(), 'ethereum', ethereum)

# Запрашиваем цены по символу и адресу контракта с разных бирж__________________________________________________________
for t in tickers_1inch:
    for e in ethereum:
        if t == e['contract_adress']:
            price_1inch = get_requested_token_prices([e['contract_adress']])
            e['price'] = price_1inch
            ethereum_1inch.append(e)
            print(e)


