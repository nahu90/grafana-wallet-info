import threading

from django.conf import settings


def run_async(function, *args):
    if settings.RUN_ASYNC:
        t = threading.Thread(target=function, args=args, kwargs={})
        t.setDaemon(True)
        t.start()
    else:
        function(*args)
