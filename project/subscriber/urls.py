from django.urls import path
from .views import SubscriptionView

urlpatterns = [
    path('subscribe/', SubscriptionView.as_view(), name='subscribe'),
    path('subscribed/', SubscriptionView.as_view(), name='subscribed'),

]
