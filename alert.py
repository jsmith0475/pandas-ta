import pandas as pd
import pandas_ta as ta
import ccxt, yfinance
import requests

exchange = ccxt.binance()

bars = exchange.fetch_ohlcv("ETH/USDT", timeframe = "5m", limit = 500)

df = pd.DataFrame(bars, columns = ["time", "open", "high", "low", "close", "volume"])


adx = df.ta.adx()
macd = df.ta.macd(fast = 14, slow = 28)
rsi = df.ta.rsi()

df = pd.concat([df, adx, macd, rsi], axis = 1)

last_row = df.iloc[-1]

WEBHOOK_URL = "https://discord.com/api/webhooks/982018197245022300/1vYv70MN3smSOQKNUmfIaImQJKDMFa5fl1NE74vRqBHifK5Bqim2z7vbfMGZnYQFWohi"

tmp = last_row["ADX_14"]
if last_row["ADX_14"] > 25:
    if last_row["DMP_14"] > last_row["DMN_14"]:
        message = f"STRONG UP TREND: The ADX is {last_row['ADX_14']: .2f} +DI {last_row['DMP_14']} -DI {last_row['DMN_14']}"
    if last_row["DMN_14"] > last_row["DMP_14"]:
        message = f"STRONG DOWN TREND: The ADX is {last_row['ADX_14']} +DI {last_row['DMP_14']} -DI {last_row['DMN_14']}"
    
    payload = {
        "username" : "alertbot",
        "content" : message
    }
    
    requests.post(WEBHOOK_URL, json = payload)

if last_row["ADX_14"] < 25:
    message = f"NO TREND: The ADX is {last_row['ADX_14']} +DI {last_row['DMP_14']} -DI {last_row['DMN_14']}"
    print(message)
    
    payload = {
        "username" : "alertbot",
        "content" : message
    }
    
    requests.post(WEBHOOK_URL, json = payload)



