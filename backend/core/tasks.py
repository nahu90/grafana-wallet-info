from backend.celery import app
from core.services.polygon_service import polygon_service
from core.services.prices_service import prices_service


@app.task(max_retries=0)
def update_wallets():
    polygon_service.update_wallets()


@app.task(max_retries=0)
def save_last_five_years_prices():
    prices_service.save_last_five_years_prices()
