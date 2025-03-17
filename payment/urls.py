from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('', views.payment_portal, name='payment_portal'),
    path('process/', views.process_payment, name='process_payment'),
]

