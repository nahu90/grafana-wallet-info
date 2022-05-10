from django.core.management.base import BaseCommand

from core.services.grafana_service import grafana_service
from core.services.prices_service import prices_service


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        # prices_service.save_prices_in_database(5)
        grafana_service.update_or_create_prices_dashboards()

