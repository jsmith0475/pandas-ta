import pandas as pd
import pandas_ta as ta
import ccxt, yfinance
import requests
import os, sys

exchange = ccxt.binance()

# Get list of symbols
dir = os.path.dirname(os.path.abspath("__file__"))
path = os.path.join(dir, 'pandas-ta', 'symbols.csv')
symbols = pd.read_csv(path)

symbols = pd.DataFrame(symbols, columns = ["symbol"])
symbols = symbols["symbol"].values.tolist()

for symbol in symbols:
    bars = exchange.fetch_ohlcv(symbol, timeframe = "5m", limit = 500)
    df = pd.DataFrame(bars, columns = ["time", "open", "high", "low", "close", "volume"])
    df['time'] = pd.to_datetime(df['time'], unit = 'ms')    
    
    # technical indicators
    adx = df.ta.adx()
    macd = df.ta.macd(fast = 14, slow = 28)
    rsi = df.ta.rsi()
    
    tenkan=9
    kijun=26
    senkou=52
    ichimoku = ta.ichimoku(df['high'], df['low'], df['close'], tenkan=tenkan, kijun = kijun, senkou = senkou)

    # create composite df
    df = pd.concat([df, adx, macd, rsi, ichimoku[0]], axis = 1)

    # grab the last value
    last_row = df.iloc[-1]
    last_row_ich_kijun = ichimoku[0].iloc[-1]
    cap_time = last_row[0]

    # hook to discord channel
    WEBHOOK_URL = "https://discord.com/api/webhooks/982327105041875004/w_ume6BIxlHe3C9jgRUrUXWSFn3oiLcvpb2118vsNh8iZdRGHxD5LqYDer2cGwsjd_sL"

    # logic
    if last_row["ADX_14"] > 25:
        if (last_row_ich_kijun['ISA_9'] > last_row_ich_kijun['ISB_26']): # future up trend
            if (last_row['close'] > last_row['ISA_9']) & (last_row['close'] > last_row['ISB_26']):
                if (row['ITS_9'] > row['IKS_26']):
                     message = f"{cap_time} STRONG UP TREND: {symbol}: The ADX is {last_row['ADX_14']: .2f} +DI {last_row['DMP_14']: .2f} -DI {last_row['DMN_14']: .2f}"
        
    if last_row["ADX_14"] > 25:
        if (last_row_ich_kijun['ISA_9'] < last_row_ich_kijun['ISB_26']): # future up trend
            if (last_row['close'] < last_row['ISA_9']) & (last_row['close'] < last_row['ISB_26']):
                if (last_row['ITS_9'] < last_row['IKS_26']):
                     message = f"{cap_time} STRONG DOWN TREND: {symbol}: The ADX is {last_row['ADX_14']: .2f} +DI {last_row['DMP_14']: .2f} -DI {last_row['DMN_14']: .2f}"
           
        payload = {
            "username" : "alertbot",
            "content" : message
        }

        print(message)
        requests.post(WEBHOOK_URL, json = payload)

    if last_row["ADX_14"] < 25:
        message = f"{cap_time} no trend:{symbol}: The ADX is {last_row['ADX_14']: .2f} +DI {last_row['DMP_14']: .2f} -DI {last_row['DMN_14']: .2f}"

        payload = {
            "username" : "alertbot",
            "content" : message
        }
        
        print(message)
        requests.post(WEBHOOK_URL, json = payload)