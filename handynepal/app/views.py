import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .models import User  # Import the custom User model
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

#user authentication    
def user_registration(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        role = request.POST['role']
        password = request.POST['password']
        confirmpassword = request.POST['confirmPassword']
        
        # Validate email format
        if not email.endswith('@gmail.com'):
            messages.error(request, 'Email must be a @gmail.com address.')
            return render(request, 'authentication/registration.html')
        
        # Validate username
        elif not re.match(r'^[a-zA-Z0-9_]+$', username):
            messages.error(request, 'Username can only contain alphanumeric characters and underscores.')
            return render(request, 'authentication/registration.html')
            
        elif username.isdigit():
            messages.error(request, 'Username cannot be only numbers.')
            return render(request, 'authentication/registration.html')

        # Validate password
        elif len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) \
                or not re.search(r'[0-9]', password) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            messages.error(request, 'Password must be at least 8 characters long, include uppercase and lowercase letters, a number, and a special character.')
            return render(request, 'authentication/registration.html')

        # Check if passwords match
        elif password != confirmpassword:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'authentication/registration.html')

        # Check if username is taken
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'authentication/registration.html')

        # Check if email is already registered
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return render(request, 'authentication/registration.html')
            
        else:
            # Create the user with full_name and phone_number
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password
            )
            user.full_name = username  # Set the full_name field
            user.phone_number = phone  # Set the phone_number field
            user.role = role  # Set the role field
            user.save()
            
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('user_login')
    
    return render(request, 'authentication/registration.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # First, try to get the user by email
        try:
            user = User.objects.get(email=email)
            # Then authenticate with the username and password
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid password. Please try again.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email. Please register first.')
        
        return render(request, 'authentication/login.html')
    
    return render(request, 'authentication/login.html')


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




