from django.urls import path
from .views import  *

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('login/', user_login, name='user_login'),
    path('registration/', user_registration, name='user_registration'),
    path('collections/', collections, name='collections'),
    path('artisans/', artisans, name='artisans'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('faq/', faq, name='faq'),
    path('shipping_returns/', shipping_returns, name='shipping_returns'),
    path('payment_info/', payment, name='app_payment'),
    path('terms_and_conditions/', terms_and_conditions, name='terms_and_conditions'),
    path('privacy_policy/', privacy_policy, name='privacy_policy'),
    path('user_logout/', user_logout, name='user_logout'),
]
