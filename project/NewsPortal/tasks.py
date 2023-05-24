from datetime import datetime, timedelta

from django.core.mail import mail_managers
from celery import shared_task
import time

from NewsPortal.models import Post


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")

    print('Hello from background task!')

@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)


def send_mails_managers():
    print('Hi managers')



