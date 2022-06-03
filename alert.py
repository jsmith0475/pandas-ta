import pandas as pd
import pandas_ta as ta
import ccxt, yfinance
import requests


exchange = ccxt.binance()

symbols = pd.DataFrame(symbols, columns = ["symbol"])
symbols = dft2["symbol"].values.tolist()

for symbol in symbols:
    bars = exchange.fetch_ohlcv(symbol, timeframe = "5m", limit = 500)
    df = pd.DataFrame(bars, columns = ["time", "open", "high", "low", "close", "volume"])

    # technical indicators
    adx = df.ta.adx()
    macd = df.ta.macd(fast = 14, slow = 28)
    rsi = df.ta.rsi()

    # create composite df
    df = pd.concat([df, adx, macd, rsi], axis = 1)

    # grab the last value
    last_row = df.iloc[-1]

    # hook to discord channel
    WEBHOOK_URL = "https://discord.com/api/webhooks/981984523317301279/AZEt7Fz5WWZoHqUgaKfczzmj7Mjf7XuumJLLss-nEFuSZ6FWE_dUWgqvzLQpTmBAoxz1"

    # logic
    if last_row["ADX_14"] > 25:
        if last_row["DMP_14"] > last_row["DMN_14"]:
            message = f"STRONG UP TREND: {symbol}: The ADX is {last_row['ADX_14']: .2f} +DI {last_row['DMP_14']: .2f} -DI {last_row['DMN_14']: .2f}"
        if last_row["DMN_14"] > last_row["DMP_14"]:
            message = f"STRONG DOWN TREND:{symbol}: The ADX is {last_row['ADX_14']: .2f} +DI {last_row['DMP_14']: .2f} -DI {last_row['DMN_14']: .2f}"

        payload = {
            "username" : "alertbot",
            "content" : message
        }

        requests.post(WEBHOOK_URL, json = payload)

    if last_row["ADX_14"] < 25:
        message = f"NO TREND:{symbol}: The ADX is {last_row['ADX_14']: .2f} +DI {last_row['DMP_14']: .2f} -DI {last_row['DMN_14']: .2f}"

        payload = {
            "username" : "alertbot",
            "content" : message
        }
        
        requests.post(WEBHOOK_URL, json = payload)