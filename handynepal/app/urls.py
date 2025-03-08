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
]
