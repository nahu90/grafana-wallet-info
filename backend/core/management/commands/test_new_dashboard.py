from django.core.management.base import BaseCommand

from core.services.grafana_service import grafana_service
from core.services.polygon_service import polygon_service
from core.services.prices_service import prices_service


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        pass
        # prices_service.save_coin_price_history_in_database()
        # polygon_service.update_wallets()make she
        grafana_service.generate_wallets_dashboards()
