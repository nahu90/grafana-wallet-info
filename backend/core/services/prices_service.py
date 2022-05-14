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

    def get_price_history(self, coin_id, years):
        now = datetime.now()
        to_timestamp = datetime.timestamp(now)
        from_timestamp = datetime.timestamp(now - relativedelta(years=years))

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

    def save_prices_in_database(self, years_to_save):
        coins = Coin.objects.filter(is_active=True)

        for coin in coins:
            price_history = self.get_price_history(coin.coingecko_id, years_to_save)
            self.save_coin_price_history(coin, price_history)

    def save_last_five_years_prices(self):
        self.save_prices_in_database(5)


prices_service = PricesService()
