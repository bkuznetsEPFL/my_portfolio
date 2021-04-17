import investpy
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def show_scatter_and_return_corr(name: str, country: str, start_date: str, end_date: str):
    BTC = investpy.get_crypto_historical_data(crypto='bitcoin',
                                              from_date=start_date,
                                              to_date=end_date)
    try:
        security = investpy.indices.get_index_historical_data(index=name,
                                                              country=country,
                                                              from_date=start_date,
                                                              to_date=end_date,
                                                              as_json=False,
                                                              order='ascending',
                                                              interval='Daily')
    except:
        security = investpy.get_stock_historical_data(stock=name,
                                                      country=country,
                                                      from_date=start_date,
                                                      to_date=end_date)
    security = security.reindex(BTC.index)
    security.fillna(value={'Volume': 0}, inplace=True)
    security.fillna(method='ffill', inplace=True)
    security.dropna(how='any', inplace=True)
    BTC = BTC.reindex(security.index)

    plt.scatter(x=BTC.Close, y=security.Close)
    plt.show()

    return security, np.round(np.corrcoef(BTC.Close, security.Close)[0, 1], 2)


def GBTC_study():
    gbtc = yf.Ticker("GBTC")
    gbtc_ohlc = gbtc.history(period="max").resample('W').sum()
    gbtc_ohlc['rets'] = np.log(gbtc_ohlc.Close).diff()

    btc = yf.Ticker("BTC-USD")
    btc_ohlc = btc.history(period="max").resample('W').sum()
    btc_ohlc['rets'] = np.log(btc_ohlc.Close).diff()

    gbtc_ohlc.dropna(inplace=True)
    btc_ohlc = btc_ohlc.reindex(gbtc_ohlc.index)

    fig = plt.figure(figsize=(15, 10))
    plt.grid()
    plt.plot(btc_ohlc.index, btc_ohlc.rets)
    plt.plot(btc_ohlc.index, gbtc_ohlc.rets)
    plt.show()

    return btc_ohlc, gbtc_ohlc


# security, corr = show_scatter_and_return_corr(name='S&P 500', country='united states',start_date='11/04/2000',
#                                               end_date='11/04/2021')

btc_ohlc, gbtc_ohlc = GBTC_study()

# checking privacy
