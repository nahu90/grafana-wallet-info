import json

import collections
import requests
from django.conf import settings
from grafanalib._gen import DashboardEncoder
from grafanalib.core import Dashboard, TimeSeries, GridPos, SqlTarget, USD_FORMAT, Time

from core.models import Coin


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
                        rawSql=f'SELECT date AS "time", price AS metric, price FROM core_coinprice WHERE coin_id = { coin.id } ORDER BY 1,2',
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

        wallet_dashboard_json = self.get_dashboard_json(dashboard, overwrite=True)
        self.upload_to_grafana(wallet_dashboard_json)

        return dashboard

    # @staticmethod
    # def update_or_create_wallets_dashboards(wallet):
    #     bitcoin_prices = coingecko_service.get_price_history('bitcoin')
    #     dashboard = Dashboard(
    #         uid=f'grafanalib-wallet-{wallet.id}',
    #         title=f'Wallet: {wallet.name} - [{wallet.address}]',
    #         description=f'Data of wallet {wallet.name} - [{wallet.address}]',
    #         tags=[
    #             'wallet'
    #         ],
    #         timezone="browser",
    #         panels=[
    #             TimeSeries(
    #                 title="Prometheus http requests",
    #                 dataSource='prometheus',
    #                 targets=[
    #                     Target(
    #                         expr='rate(prometheus_http_requests_total[5m])',
    #                         legendFormat="{{ handler }}",
    #                         refId='A',
    #                     ),
    #                 ],
    #                 unit=OPS_FORMAT,
    #                 gridPos=GridPos(h=8, w=16, x=0, y=10),
    #             ),
    #         ],
    #     )
    #
    #     return dashboard
    #
    # def generate_wallets_dashboards(self):
    #     wallets = Wallet.objects.filter(is_active=True)
    #     for wallet in wallets:
    #         wallet_dashboard = self.get_wallet_dashboard(wallet)
    #         wallet_dashboard_json = self.get_dashboard_json(wallet_dashboard, overwrite=True)
    #         self.upload_to_grafana(wallet_dashboard_json)

grafana_service = GrafanaService()
