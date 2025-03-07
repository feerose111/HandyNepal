from django.shortcuts import render , redirect

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

def home1(request):
    return render(request, 'home1.html')

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')


