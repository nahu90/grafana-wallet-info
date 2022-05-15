from celery.schedules import crontab

beat_schedule = {
    'update-wallets': {
       'task': 'core.tasks.update_wallets',
       'schedule': crontab(hour='*/1', minute='10'),
    },
    'save-last-five-years-prices': {
        'task': 'core.tasks.save_last_five_years_prices',
        'schedule': crontab(hour='*/1', minute='20'),
    },
    'generate-wallets-dashboards': {
        'task': 'core.tasks.generate_wallets_dashboards',
        'schedule': crontab(hour='*/1', minute='30'),
    }
}
