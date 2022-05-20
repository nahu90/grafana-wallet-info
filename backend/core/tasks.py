from backend.celery import app
from core.services.grafana_service import grafana_service
from core.services.polygon_service import polygon_service
from core.services.prices_service import prices_service


@app.task(max_retries=0)
def update_wallets():
    polygon_service.update_wallets()


@app.task(max_retries=0)
def save_coin_price_history_in_database():
    prices_service.save_coin_price_history_in_database()


@app.task(max_retries=0)
def generate_wallets_dashboards():
    grafana_service.generate_wallets_dashboards()
