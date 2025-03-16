import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone
from decimal import Decimal
from .models import User, Contact, Artisan, Product# Import the custom User model and Order models
from django.core.paginator import Paginator
# Create your views here.

def home(request):
    
    return render(request, 'main/home.html')

def collections(request):
    # Get all products
    products = Product.objects.all()
    # Get all artisans for the filter
    all_artisans = Artisan.objects.all()
    
    # Get filter parameters from request
    category = request.GET.getlist('category')
    artisan = request.GET.getlist('artisan')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort_by')
    is_ajax = request.GET.get('ajax') == 'true'
    
    # Apply filters if provided
    if category:
        products = products.filter(category__in=category)
    
    if artisan:
        # Split artisan names and filter by first name
        artisan_first_names = [a.split('-')[0] for a in artisan if '-' in a]
        if artisan_first_names:
            products = products.filter(artisan__first_name__icontains=artisan_first_names[0])
    
    if min_price:
        try:
            min_price = float(min_price)
            products = products.filter(price__gte=min_price)
        except (ValueError, TypeError):
            pass
    
    if max_price:
        try:
            max_price = float(max_price)
            products = products.filter(price__lte=max_price)
        except (ValueError, TypeError):
            pass
    
    # Apply sorting
    if sort_by:
        if sort_by == 'price-low':
            products = products.order_by('price')
        elif sort_by == 'price-high':
            products = products.order_by('-price')
        elif sort_by == 'newest':
            products = products.order_by('-created_at')
        elif sort_by == 'bestselling':
            # First get bestsellers, then non-bestsellers
            bestsellers = products.filter(is_bestseller=True)
            non_bestsellers = products.filter(is_bestseller=False)
            products = list(bestsellers) + list(non_bestsellers)
        elif sort_by == 'featured':
            # First get featured, then non-featured
            featured = products.filter(is_featured=True)
            non_featured = products.filter(is_featured=False)
            products = list(featured) + list(non_featured)
    
    # If this is an AJAX request, render only the product grid
    if is_ajax:
        return render(request, 'main/partials/product_grid.html', {'products': products})
    
    return render(request, 'main/collections.html', {'products': products, 'all_artisans': all_artisans})

def artisans(request):
    artisans = Artisan.objects.all()
    return render(request, 'main/artisans.html', {'artisans': artisans})

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        created_at = timezone.now()
        
        #save the data to the database
        Contact.objects.create(name=name, email=email, phone=phone, message=message, created_at=created_at)
        messages.success(request, 'Message sent successfully!')
        return redirect('contact') 
    
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

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


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




