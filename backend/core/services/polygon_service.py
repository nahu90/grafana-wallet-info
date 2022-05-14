import json
from datetime import timezone

from django.conf import settings
from django.utils import timezone
from web3 import Web3

from core.models import Coin, Wallet, WalletCoinBalance
from core.services.prices_service import prices_service


class PolygonService:
    w3 = None

    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.WEB3_INFURA_POLYGON_URL))

    def save_token_balance_from_contract(self, coin, wallet):
        token = self.w3.eth.contract(
            address=Web3.toChecksumAddress(coin.polygon_contract_address),
            abi=json.loads(coin.contract_abi)
        )
        token_balance = token.functions.balanceOf(Web3.toChecksumAddress(wallet.address)).call()
        decimals = token.functions.decimals().call()

        wallet_coin_balance = WalletCoinBalance(
            wallet=wallet,
            coin=coin,
            balance=(token_balance / (10 ** decimals)),
            date=timezone.now()
        )
        wallet_coin_balance.save()

        usd_price = prices_service.get_actual_price(coin.coingecko_id)
        wallet_coin_balance.usd_balance = usd_price * wallet_coin_balance.balance
        wallet_coin_balance.save()

    def save_matic_balance(self, wallet):
        token_balance = self.w3.eth.get_balance(Web3.toChecksumAddress(wallet.address))

        wallet_coin_balance = WalletCoinBalance(
            wallet=wallet,
            coin=Coin.objects.get(name='MATIC'),
            balance=self.w3.fromWei(token_balance, 'ether'),
            date=timezone.now()
        )
        wallet_coin_balance.save()

        usd_price = prices_service.get_actual_price('wmatic')
        wallet_coin_balance.usd_balance = usd_price * float(wallet_coin_balance.balance)
        wallet_coin_balance.save()

    def update_wallet_balance(self, wallet):
        coins = Coin.objects.filter(is_active=True).exclude(name__in=['MATIC', ])
        for coin in coins:
            self.save_token_balance_from_contract(coin, wallet)
        self.save_matic_balance(wallet)

    def update_wallets(self):
        wallets = Wallet.objects.filter(is_active=True)
        for wallet in wallets:
            self.update_wallet_balance(wallet)

polygon_service = PolygonService()
