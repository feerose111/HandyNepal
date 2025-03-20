from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('collections/', views.collections, name='collections'),
    path('artisans/', views.artisans, name='artisans'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),

    # Authentication
    path('user/register/', views.user_registration, name='user_registration'),
    path('user/login/', views.user_login, name='user_login'),
    path('user/logout/', views.user_logout, name='user_logout'),

    # Cart URLs
    path('cart/', views.cart, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),

    # Help Pages
    path('help/faq/', views.faq, name='faq'),
    path('help/shipping-returns/', views.shipping_returns, name='shipping_returns'),
    path('help/payment/', views.payment, name='app_payment'),
    path('help/terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('help/privacy-policy/', views.privacy_policy, name='privacy_policy'),

    # Payment
    path('payment/portal/', views.payment_portal, name='payment_portal'),
]
