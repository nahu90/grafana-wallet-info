from django.core.management.base import BaseCommand

from core.services.grafana_service import grafana_service
from core.services.polygon_service import polygon_service
from core.services.prices_service import prices_service


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        pass
        # prices_service.save_last_five_years_prices()
        grafana_service.update_or_create_prices_dashboards()
        # polygon_service.test()


