import json
from datetime import timezone

from django.conf import settings
from django.utils import timezone
from web3 import Web3

from core.models import Coin, Wallet, WalletCoinBalance, COIN_TYPE, WalletTotalBalance
from core.services.prices_service import prices_service


class PolygonService:
    w3 = None

    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.WEB3_INFURA_POLYGON_URL))

    def save_token_balance_from_contract(self, coin, wallet, wallet_total_balance_id):
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

        try:
            usd_price = prices_service.get_actual_price(coin.coingecko_id)
            wallet_coin_balance.usd_balance = usd_price * wallet_coin_balance.balance
            wallet_coin_balance.save()

            wallet_total_balance = WalletTotalBalance.objects.get(pk=wallet_total_balance_id)
            wallet_total_balance.usd_balance = wallet_total_balance.usd_balance + wallet_coin_balance.usd_balance
            wallet_total_balance.save()
        except Exception as e:
            print(e)

    def save_matic_balance(self, wallet, wallet_total_balance_id):
        token_balance = self.w3.eth.get_balance(Web3.toChecksumAddress(wallet.address))

        wallet_coin_balance = WalletCoinBalance(
            wallet=wallet,
            coin=Coin.objects.get(type=COIN_TYPE.POLYGON),
            balance=self.w3.fromWei(token_balance, 'ether'),
            date=timezone.now()
        )
        wallet_coin_balance.save()

        try:
            usd_price = prices_service.get_actual_price('wmatic')
            wallet_coin_balance.usd_balance = usd_price * float(wallet_coin_balance.balance)
            wallet_coin_balance.save()

            wallet_total_balance = WalletTotalBalance.objects.get(pk=wallet_total_balance_id)
            wallet_total_balance.usd_balance = wallet_total_balance.usd_balance + wallet_coin_balance.usd_balance
            wallet_total_balance.save()
        except Exception as e:
            print(e)

    def save_aave_atoken_balance(self, wallet, atoken, wallet_total_balance_id):
        token = self.w3.eth.contract(
            address=Web3.toChecksumAddress(atoken.polygon_contract_address),
            abi=json.loads(atoken.contract_abi)
        )
        token_balance = token.functions.balanceOf(Web3.toChecksumAddress(wallet.address)).call()
        decimals = token.functions.decimals().call()

        wallet_coin_balance = WalletCoinBalance(
            wallet=wallet,
            coin=atoken,
            balance=(token_balance / (10 ** decimals)),
            date=timezone.now()
        )
        wallet_coin_balance.save()

        try:
            usd_price = prices_service.get_actual_price(atoken.coingecko_id)
            wallet_coin_balance.usd_balance = usd_price * wallet_coin_balance.balance
            wallet_coin_balance.save()

            wallet_total_balance = WalletTotalBalance.objects.get(pk=wallet_total_balance_id)
            wallet_total_balance.usd_balance = wallet_total_balance.usd_balance + wallet_coin_balance.usd_balance
            wallet_total_balance.save()
        except Exception as e:
            print(e)

    def save_aave_balance(self, wallet, wallet_total_balance_id):
        atokens = Coin.objects.filter(type=COIN_TYPE.ATOKEN, is_active=True)
        for atoken in atokens:
            self.save_aave_atoken_balance(wallet, atoken, wallet_total_balance_id)

    def save_erc20_balance(self, wallet, wallet_total_balance_id):
        coins = Coin.objects.filter(type=COIN_TYPE.ERC_20, is_active=True)
        for coin in coins:
            self.save_token_balance_from_contract(coin, wallet, wallet_total_balance_id)

    def update_wallet_balance(self, wallet):
        wallet_total_balance = WalletTotalBalance(
            wallet=wallet,
            usd_balance=0,
            date=timezone.now(),
            is_active=False
        )
        wallet_total_balance.save()

        self.save_erc20_balance(wallet, wallet_total_balance.id)
        self.save_matic_balance(wallet, wallet_total_balance.id)
        self.save_aave_balance(wallet, wallet_total_balance.id)

        wallet_total_balance = WalletTotalBalance.objects.get(pk=wallet_total_balance.id)
        wallet_total_balance.is_active = True
        wallet_total_balance.save()

    def update_wallets(self):
        wallets = Wallet.objects.filter(is_active=True)
        for wallet in wallets:
            self.update_wallet_balance(wallet)

polygon_service = PolygonService()
