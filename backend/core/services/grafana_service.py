import collections
import json

import requests
from django.conf import settings
from grafanalib._gen import DashboardEncoder
from grafanalib.core import Dashboard, TimeSeries, GridPos, SqlTarget, USD_FORMAT, Time, Stat, Threshold

from core.models import Coin, Wallet, COIN_TYPE, WalletCoinBalance


class GrafanaService:
    GRAFANA_HOST = None
    GRAFANA_API_KEY = None

    def __init__(self):
        self.GRAFANA_HOST = settings.GRAFANA_HOST
        self.GRAFANA_API_KEY = settings.GRAFANA_API_KEY

    def upload_to_grafana(self, json, verify=True):
        headers = {'Authorization': f"Bearer {self.GRAFANA_API_KEY}", 'Content-Type': 'application/json'}
        r = requests.post(f"{self.GRAFANA_HOST}/api/dashboards/db", data=json, headers=headers, verify=verify)
        print(f"{r.status_code} - {r.content}")

    @staticmethod
    def get_dashboard_json(dashboard, overwrite=False, message="Updated by grafanlib"):
        dashboard_dict = {
            "dashboard": dashboard.to_json_data(),
            "overwrite": overwrite,
            "message": message
        }

        get_dashboard_json = json.dumps(dashboard_dict, sort_keys=True, indent=2, cls=DashboardEncoder)

        return get_dashboard_json

    @staticmethod
    def generate_coins_prices_panels():
        panels = []
        coins = Coin.objects.filter(is_active=True)
        x_positions = collections.deque([0, 8, 16])
        for i, coin in enumerate(coins):
            panel = TimeSeries(
                title=f'{coin.name} Prices',
                dataSource='django-postgresql',
                targets=[
                    SqlTarget(
                        rawSql=f'SELECT date AS "time", price FROM core_coinprice WHERE coin_id = { coin.id } ORDER BY 1',
                        refId="A",
                    ),
                ],
                unit=USD_FORMAT,
                gridPos=GridPos(h=8, w=8, x=x_positions[0], y=0),
            )
            panels.append(panel)
            x_positions.rotate(1)

        return panels

    def update_or_create_prices_dashboards(self):
        dashboard = Dashboard(
            time=Time('now-1y', 'now'),
            uid=f'coin_prices',
            title='Coin Prices',
            description=f'Prices of coins obtained from coingecko',
            tags=[
                'coin',
                'prices'
            ],
            timezone="browser",
            panels=self.generate_coins_prices_panels(),
        )

        prices_dashboard_json = self.get_dashboard_json(dashboard, overwrite=True)
        self.upload_to_grafana(prices_dashboard_json)

        return dashboard

    @staticmethod
    def get_wallet_last_balance_panels(wallet):
        panels = []
        coins = Coin.objects.filter(type__in=[COIN_TYPE.POLYGON, COIN_TYPE.ERC_20, COIN_TYPE.ATOKEN], is_active=True)
        x_positions = collections.deque([0, 3, 6, 9, 12, 15, 18, 21])
        for i, coin in enumerate(coins, 1):
            if WalletCoinBalance.objects.filter(wallet=wallet, coin=coin).order_by('-date').first().balance <= 0:
                continue

            panel = Stat(
                title=f'{coin.name} Balance',
                dataSource='django-postgresql',
                colorMode='value',
                reduceCalc='last',
                targets=[
                    SqlTarget(
                        rawSql=f'SELECT date as time, balance as {coin.name} FROM core_walletcoinbalance WHERE coin_id = {coin.id} AND wallet_id = {wallet.id} ORDER BY 1',
                        refId=f'A-{i}',
                    ),
                    SqlTarget(
                        rawSql=f'SELECT date as time, usd_balance as usd FROM core_walletcoinbalance WHERE coin_id = {coin.id} AND wallet_id = {wallet.id} ORDER BY 1',
                        refId=f'A-usd-{i}',
                    ),
                ],
                thresholds=[
                    Threshold(
                        color='gray',
                        index=1,
                        value=0.0,
                        op='gt',
                        yaxis='right'
                    ),
                    Threshold(
                        color='green',
                        index=1,
                        value=0.000000001,
                        op='gt',
                        yaxis='right'
                    ),
                ],
                gridPos=GridPos(h=4, w=3, x=x_positions[0], y=0),
            )
            panels.append(panel)
            x_positions.rotate(1)

        return panels

    @staticmethod
    def get_wallet_balance_timeline_panel(wallet):
        targets_for_timeseries = []
        coins = Coin.objects.filter(type__in=[COIN_TYPE.POLYGON, COIN_TYPE.ERC_20, COIN_TYPE.ATOKEN], is_active=True)
        for i, coin in enumerate(coins, 1):
            targets_for_timeseries.append(
                SqlTarget(
                    rawSql=f'SELECT date as time, usd_balance as {coin.name} FROM core_walletcoinbalance WHERE coin_id = {coin.id} AND wallet_id = {wallet.id} ORDER BY 1',
                    refId=f'B-{i}',
                )
            )

        panel = TimeSeries(
            title=f'Balances timeseries',
            dataSource='django-postgresql',
            lineWidth=2,
            pointSize=8,
            showPoints='always',
            targets=targets_for_timeseries,
            unit=USD_FORMAT,
            gridPos=GridPos(h=14, w=24, x=0, y=10),
        )

        return panel

    def get_wallet_last_total_balance_panels(self, wallet):
        panel = Stat(
            title=f'Total Balance',
            dataSource='django-postgresql',
            colorMode='value',
            reduceCalc='last',
            targets=[
                SqlTarget(
                    rawSql=f'SELECT date as time, usd_balance as usd FROM core_wallettotalbalance WHERE wallet_id = {wallet.id} ORDER BY 1',
                    refId=f'A-usd-Total',
                ),
            ],
            thresholds=[
                Threshold(
                    color='gray',
                    index=1,
                    value=0.0,
                    op='gt',
                    yaxis='right'
                ),
                Threshold(
                    color='green',
                    index=1,
                    value=0.000000001,
                    op='gt',
                    yaxis='right'
                ),
            ],
            gridPos=GridPos(h=4, w=3, x=0, y=0),
        )

        return panel

    def update_or_create_wallets_dashboards(self, wallet):
        panels = []
        panels.append(self.get_wallet_last_total_balance_panels(wallet))
        panels.extend(self.get_wallet_last_balance_panels(wallet))
        panels.append(self.get_wallet_balance_timeline_panel(wallet))

        dashboard = Dashboard(
            time=Time('now-12h', 'now'),
            uid=f'grafanalib-wallet-{wallet.id}',
            title=f'Wallet: {wallet.name} - [{wallet.address}]',
            description=f'Data of wallet {wallet.name} - [{wallet.address}]',
            tags=[
                'wallet'
            ],
            timezone="browser",
            panels=panels
        )

        return dashboard

    def generate_wallets_dashboards(self):
        wallets = Wallet.objects.filter(is_active=True)
        for wallet in wallets:
            wallet_dashboard = self.update_or_create_wallets_dashboards(wallet)
            wallet_dashboard_json = self.get_dashboard_json(wallet_dashboard, overwrite=True)
            self.upload_to_grafana(wallet_dashboard_json)

grafana_service = GrafanaService()
