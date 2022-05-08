from celery.schedules import crontab

beat_schedule = {
    'test-task': {
       'task': 'core.tasks.test_task',
       'schedule': crontab(hour='00', minute='00'),
    },
}
