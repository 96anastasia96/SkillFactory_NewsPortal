from django.core.mail import mail_managers
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Post


@receiver(post_save, sender=Post)
def notify_managers(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.title}'
    else:
        subject = f'Пост был изменен{instance.title} {instance.text}'

    mail_managers(
        subject=subject,
        message=instance.text,
    )
    print(f'{instance.title}')


post_save.connect(notify_managers, sender=Post)


@receiver(post_delete, sender=Post)
def notify_managers_post_deleted(sender, instance, **kwargs):
    subject = f'Пост с названием "{instance.title}" был удален'
    mail_managers(
        subject=subject,
        message=f'Текст: {instance.text} ',
    )

    print(subject)