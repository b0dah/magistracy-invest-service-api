import time
from datetime import datetime

import numpy as np
import schedule
import ujson
from pycoingecko import CoinGeckoAPI


def update_symbols():
    print(f"Updating symbols. Time = {datetime.now()}")
    cg = CoinGeckoAPI()

    with open('data/db/allowed_symbols.json', 'r') as file:
        allowed_coins = ujson.loads(file.read())

    result = []

    params = {
        "localization": False,
        "tickers": False,
        "market_data": True,
        "community_data": False,
        "developer_data": False,
        "sparkline": False
    }

    for coin in allowed_coins:
        print(f"Check coin: {coin}")
        detail_coin = cg.get_coin_by_id(coin.get('id'), **params)

        filter_detail_coin = {
            "name": detail_coin['name'],
            "symbol": detail_coin['symbol'],
            "id": detail_coin['id'],
            "price": detail_coin["market_data"]['current_price']['usd'],
            "market_cap": detail_coin["market_data"]['market_cap']['usd'],
            "total_volume": detail_coin["market_data"]['total_volume']['usd'],
            "pr_ch_perc_7d": detail_coin["market_data"]['price_change_percentage_7d'],
            "pr_ch_perc_14d": detail_coin["market_data"]['price_change_percentage_14d'],
            "pr_ch_perc_30d": detail_coin["market_data"]['price_change_percentage_30d'],
            "pr_ch_perc_60d": detail_coin["market_data"]['price_change_percentage_60d'],
            "pr_ch_perc_200d": detail_coin["market_data"]['price_change_percentage_200d'],
            "pr_ch_perc_1y": detail_coin["market_data"]['price_change_percentage_1y'],
        }
        result.append(filter_detail_coin)

    with open('data/db/detail_symbols.json', 'w') as file:
        allowed_coins = file.write(ujson.dumps(result))


def update_charts():
    print(f"Updating charts. Time = {datetime.now()}")
    cg = CoinGeckoAPI()

    with open('data/db/allowed_symbols.json', 'r') as file:
        allowed_coins = ujson.loads(file.read())

    result = {}

    params = {
        "vs_currency": "usd",
        "days": 1825  # 5 years is 1825 days
    }

    for coin in allowed_coins:
        print(f"Check coin: {coin}")
        prices = cg.get_coin_market_chart_by_id(coin.get('id'), **params)
        # print(coin, len(prices['prices']))
        result[coin['id']] = {
            "prices": [],
            "profits": [],
        }

        for price in prices['prices']:
            result[coin['id']]["prices"].append(price[1])

    with open('data/db/charts.json', 'w') as file:
        file.write(ujson.dumps(result))


def prepair_calculation():
    print(f"Preparing calculation. Time = {datetime.now()}")

    with open('data/db/charts.json', 'r') as file:
        charts = ujson.loads(file.read())

    for coin in charts:
        for i in range(len(charts[coin]["prices"]) - 1):
            profit = (charts[coin]["prices"][i + 1] - charts[coin]["prices"][i]) \
                     / charts[coin]["prices"][i]
            charts[coin]["profits"].append(profit)
        charts[coin]["general_profit"] = np.mean(charts[coin]["profits"])
        charts[coin]["general_risk"] = np.std(charts[coin]["profits"])

    with open('data/db/charts.json', 'w') as file:
        file.write(ujson.dumps(charts))


# Prod configuration
# schedule.every().day.at('00:01').do(update_symbols)
# schedule.every().day.at('00:02').do(update_charts)

# Test configuration
# schedule.every().minute.do(update_symbols)
# schedule.every(2).minute.do(update_charts)

if __name__ == "__main__":
    while True:
        # update_symbols()
        # time.sleep(5)
        # update_charts()
        # time.sleep(5)
        # prepair_calculation()
        schedule.run_pending()
        time.sleep(1)
