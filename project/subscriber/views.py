from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import View
from datetime import datetime
from .models import Subscription


# Create your views here.


class SubscriptionView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'subscribe.html', {})

    def post(self, request, *args, **kwargs):
        subscription = Subscription(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            user_name=request.POST['user_name'],
            message=request.POST['message'],
        )
        subscription.save()

        send_mail(
            subject=f'{subscription.user_name} {subscription.date.strftime("%Y-%M-%d")}',
            # имя клиента и дата записи будут в теме для удобства
            message=subscription.message,  # сообщение с кратким описанием проблемы
            from_email='su8scriber@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list=[]  # здесь список получателей. Например, секретарь, сам врач и т. д.
        )

        return redirect('/subscribed/')
