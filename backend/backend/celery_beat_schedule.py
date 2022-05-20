from celery.schedules import crontab

beat_schedule = {
    'update-wallets': {
       'task': 'core.tasks.update_wallets',
       'schedule': crontab(hour='*/1', minute='10'),
    },
    'save-coin-price-history-in-database': {
        'task': 'core.tasks.save_coin_price_history_in_database',
        'schedule': crontab(hour='*/1', minute='20'),
    },
    'generate-wallets-dashboards': {
        'task': 'core.tasks.generate_wallets_dashboards',
        'schedule': crontab(hour='*/1', minute='30'),
    }
}

