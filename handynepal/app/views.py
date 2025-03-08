from django.shortcuts import render , redirect

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

def collections(request):
    return render(request, 'main/collections.html')

def artisans(request):
    return render(request, 'main/artisans.html')

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')

def user_login(request):
    return render(request, 'authentication/login.html')

def user_registration(request):
    return render(request, 'authentication/registration.html')


