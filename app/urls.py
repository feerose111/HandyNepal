from django.urls import path , include
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
    path('payment/initialize_payment/', views.initialize_payment, name='initialize_payment'),
    path('payment/verify/', views.verify, name='verify'),
    
    # Order
    path('user/dashboard/track_order/', views.track_order, name='track_order'),
    path('user/dashboard/process_order/', views.process_order, name='process_order'),
    
    # Add product and artisan
    path('user/dashboard/add_product/', views.add_product, name='add_product'),
    path('user/dashboard/add_artisan/', views.add_artisan, name='add_artisan'),
    path('user/dashboard/edit_artisan/<int:artisan_id>/', views.edit_artisan, name='edit_artisan'),
    path('user/dashboard/delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('user/dashboard/edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    
        
    
]
