import json

from django.conf import settings
from web3 import Web3

from core.models import Coin, Wallet, WalletCoinBalance


class PolygonService:
    w3 = None

    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.WEB3_INFURA_POLYGON_URL))

    def get_token_balance_from_contract(self, coin, wallet):
        token = self.w3.eth.contract(
            address=Web3.toChecksumAddress(coin.polygon_contract_address),
            abi=json.loads(coin.contract_abi)
        )
        token_balance = token.functions.balanceOf(Web3.toChecksumAddress(wallet.address)).call()
        decimals = token.functions.decimals().call()

        wallet_coin_balance = WalletCoinBalance(
            wallet=wallet,
            coin=coin,
            balance=(token_balance / (10 ** decimals))
        )
        wallet_coin_balance.save()

    def update_wallet_balance(self, wallet):
        coins = Coin.objects.filter(is_active=True).exclude(coingecko_id__in=['ethereum', 'polygon'])
        for coin in coins:
            self.get_token_balance_from_contract(coin, wallet)

    def update_wallets(self):
        wallets = Wallet.objects.filter(is_active=True)
        for wallet in wallets:
            self.update_wallet_balance(wallet)

polygon_service = PolygonService()
