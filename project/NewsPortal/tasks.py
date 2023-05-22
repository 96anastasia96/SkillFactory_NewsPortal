from django.core.mail import mail_managers


def send_mails():
    print('Hello from background task!')


def send_mails_managers():
    print('Hi managers')