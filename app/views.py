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

def user_dashboard(request):
    return render(request, 'main/dashboard.html')

def user_login(request):
    return render(request, 'authentication/login.html')

def user_registration(request):
    return render(request, 'authentication/registration.html')


#help section

def faq(request):
    return render(request, 'help/faq.html')

def shipping_returns(request):
    return render(request, 'help/shipping_returns.html')

def payment(request):
    return render(request, 'help/payment.html')

def terms_and_conditions(request):
    return render(request, 'help/terms_and_conditions.html')

def privacy_policy(request):
    return render(request, 'help/privacy_policy.html')




