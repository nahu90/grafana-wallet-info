from datetime import datetime

from dateutil.relativedelta import relativedelta
from pycoingecko import CoinGeckoAPI

from core.models import Coin, CoinPrice


class PricesService:
    coingecko_api = None

    def __init__(self):
        self.coingecko_api = CoinGeckoAPI()

    def get_actual_price(self, coin_id):
        price = self.coingecko_api.get_price(
            coin_id,
            vs_currencies='usd'
        )

        return price[coin_id]['usd']

    def get_price_history(self, coin_id, date_start):
        from_timestamp = int(datetime.timestamp(date_start))
        to_timestamp = int(datetime.timestamp(datetime.now()))

        prices_history = self.coingecko_api.get_coin_market_chart_range_by_id(
            coin_id,
            vs_currency='usd',
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp
        )

        return prices_history

    @staticmethod
    def save_coin_price_history(coin, price_history):
        for price in price_history['prices']:
            coin_price = CoinPrice.objects.filter(
                coin=coin,
                date=datetime.fromtimestamp(int(price[0]) / 1000).date()
            ).first()

            if not coin_price:
                coin_price = CoinPrice(
                    coin=coin,
                    date=datetime.fromtimestamp(int(price[0]) / 1000).date()
                )

            coin_price.price = price[1]
            coin_price.save()

    def save_coin_price_history_in_database(self):
        coins = Coin.objects.filter(is_active=True)

        for coin in coins:
            date_start = datetime.now() - relativedelta(years=8)
            last_coin_price = CoinPrice.objects.filter(coin=coin).order_by('-date').first()
            if last_coin_price:
                date_start = datetime.combine(last_coin_price.date, datetime.min.time())

            try:
                price_history = self.get_price_history(coin.coingecko_id, date_start)
                self.save_coin_price_history(coin, price_history)
            except Exception as e:
                print(e)


prices_service = PricesService()
