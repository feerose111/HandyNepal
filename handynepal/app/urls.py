from django.urls import path
from .views import  *

urlpatterns = [
    path('', home, name='home'),
    path('home1/', home1, name='home1'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

]
