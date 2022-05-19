from django.core.management.base import BaseCommand

from core.services.grafana_service import grafana_service
from core.services.polygon_service import polygon_service
from core.services.prices_service import prices_service


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        pass
        prices_service.save_last_five_years_prices()
        polygon_service.update_wallets()
        grafana_service.generate_wallets_dashboards()
