import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpRequest , HttpResponse
from datetime import datetime
from django.utils import timezone
from .models import User, Contact, Artisan, Product# Import the custom User model and Order models
from django.core.paginator import Paginator
import uuid
import json, requests
from django.conf import settings

LIVE_SECRET_KEY = settings.LIVE_SECRET_KEY
# Create your views here.

def home(request):
    return render(request, 'main/home.html')

def collections(request):
    # Get all products
    products = Product.objects.all()
    
    # Filter by category if specified
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)
    
    # Sort products based on user selection
    sort = request.GET.get('sort', 'newest')  # Default sort by newest
    if sort == 'newest':
        products = products.order_by('-is_new', '-created_at')
    elif sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')
    
    # Pagination
    try:
        page = int(request.GET.get('page', 1))
    except (ValueError, TypeError):
        page = 1
    
    # Ensure page is never less than 1
    if page < 1:
        page = 1
    
    items_per_page = 4
    paginator = Paginator(products, items_per_page)
    
    # Get the page, handling case where page is out of range
    try:
        products_paginated = paginator.page(page)
    except:
        # If page is out of range, deliver last page
        products_paginated = paginator.page(paginator.num_pages)
    
    context = {
        'products': products_paginated,
        'items_per_page': items_per_page,
        'total_products': len(products),
    }
    
    return render(request, 'main/collections.html', context)

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

def payment_portal(request):
    cart_items = []
    total = 0
    item_count = 0
    
    if 'cart' in request.session:
        cart = request.session['cart']
        for product_id, item_data in cart.items():
            product = get_object_or_404(Product, id=product_id)
            quantity = item_data['quantity']
            
            # Calculate price based on whether there's a discount
            if product.is_discount and product.discount_price:
                price = float(product.discount_price)
            else:
                price = float(product.price)
                
            item_total = price * quantity 
            total += item_total
            item_count += quantity
            
            item = {
                'id': product_id,
                'name': product.name,
                'product': product,
                'quantity': quantity,
                'price': price,
                'total': item_total
            }
            cart_items.append(item)
    
    total_amount = int(total  * 100) #converting rupees to paisa
     
    
    payURL = 'https://dev.khalti.com/api/v2/'
    uid = str(uuid.uuid4())
    print(uid)
    
    context = {
        'cart_items': cart_items,
        'payURL': payURL,
        'total': total,
        'item_count': item_count,
        'total_amount': total_amount,
        'uid': uid,
    }
    
    return render(request, 'payment/payment_portal.html', context)
def initialize_payment(request):
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    
    # Get the host for constructing full URLs
    host = request.get_host()
    
    # Properly form the return_url with the full path
    return_url = f"http://{host}/payment/verify/"
    website_url = f"http://{host}"
    
    amount = request.POST.get('amount')
    purchase_order_id = request.POST.get('purchase_order_id')
    
    # Print debug information
    print(f"Return URL: {return_url}")
    print(f"Website URL: {website_url}")
    print(f"Amount: {amount}")
    print(f"Order ID: {purchase_order_id}")
    
    payload = json.dumps({
        "return_url": return_url,
        "website_url": website_url,
        "amount": amount,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": "test",
        "customer_info": {
        "name": "Handy Nepal",
        "email": "mew04804@gmail.com",
        "phone": "9800000001"
        }
    })
    
    headers = {
        'Authorization': LIVE_SECRET_KEY,
        'Content-Type': 'application/json',
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    new_res = json.loads(response.text)
    print(new_res)
    return redirect(new_res['payment_url'])
    

def verify(request):
    """Verify Khalti payment status using lookup API"""
    if request.method == 'GET':
        # Get parameters from the Khalti callback
        pidx = request.GET.get('pidx')
        status = request.GET.get('status')
        transaction_id = request.GET.get('transaction_id')
        amount = request.GET.get('amount')
        mobile = request.GET.get('mobile')
        purchase_order_id = request.GET.get('purchase_order_id')
        
        if not pidx:
            messages.error(request, "Payment verification failed: Missing payment identifier")
            return redirect('cart')
        
        # Lookup URL for payment verification
        url = "https://a.khalti.com/api/v2/epayment/lookup/"
        
        # Prepare headers and data
        headers = {
            'Authorization': LIVE_SECRET_KEY,
            'Content-Type': 'application/json',
        }
        
        data = json.dumps({
            'pidx': pidx
        })
        
        try:
            # Make verification request to Khalti
            response = requests.post(url, headers=headers, data=data)
            response_data = response.json()
            
            # Check payment status from lookup API
            lookup_status = response_data.get('status')
            transaction_id = response_data.get('transaction_id')
            amount = response_data.get('total_amount')
            
            # If payment is complete, process the order
            if lookup_status == 'Completed':
                # Payment successful, process the order
                messages.success(request, "Payment successful! Your order has been placed.")
                
                # Clear the cart
                if 'cart' in request.session:
                    del request.session['cart']
                    request.session.modified = True
                
                return redirect('home')
                
            elif lookup_status == 'Pending':
                # Payment is pending
                messages.info(request, "Your payment is being processed. We'll update you once confirmed.")
                return redirect('cart')
                
            elif lookup_status in ['Refunded', 'Expired', 'User canceled']:
                # Payment failed or canceled
                messages.error(request, f"Payment {lookup_status.lower()}. Please try again.")
                return redirect('cart')
                
            else:
                # Unknown status
                messages.error(request, f"Payment verification returned unknown status: {lookup_status}. Please contact support.")
                return redirect('cart')
                
        except Exception as e:
            # Handle request exceptions
            print(f"Exception during verification: {str(e)}")
            messages.error(request, f"Payment verification failed: {str(e)}")
            return redirect('cart')
    
    
    return redirect('payment_portal')

# Cart Views
def cart(request):
    """View to display the cart contents"""
    cart_items = []
    total = 0
    item_count = 0
    
    if 'cart' in request.session:
        cart = request.session['cart']
        for product_id, item_data in cart.items():
            product = get_object_or_404(Product, id=product_id)
            quantity = item_data['quantity']
            
            # Calculate price based on whether there's a discount
            if product.is_discount and product.discount_price:
                price = float(product.discount_price)
            else:
                price = float(product.price)
                
            item_total = price * quantity
            total += item_total
            item_count += quantity
            
            cart_items.append({
                'id': product_id,
                'product': product,
                'quantity': quantity,
                'price': price,
                'total': item_total
            })
    
    # Format total to 2 decimal places
    total = round(total, 2)
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'item_count': item_count
    }
    
    return render(request, 'Cart/cart.html' , context)

def add_to_cart(request):
    """Add a product to the cart"""
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        # Get the product to check if it exists and has enough stock
        product = get_object_or_404(Product, id=product_id)
        
        # Check if product has enough stock
        if product.stock < quantity:
            messages.error(request, f"Sorry, we only have {product.stock} of this item in stock.")
            return redirect('collections')
        
        # Initialize the cart if it doesn't exist
        if 'cart' not in request.session:
            request.session['cart'] = {}
            
        cart = request.session['cart']
        
        # Add product to cart or update quantity if already in cart
        if product_id in cart:
            # Check if the new total quantity exceeds stock
            new_quantity = cart[product_id]['quantity'] + quantity
            if new_quantity > product.stock:
                messages.error(request, f"Cannot add more. You already have {cart[product_id]['quantity']} in your cart and we only have {product.stock} in stock.")
                return redirect('collections')
            cart[product_id]['quantity'] = new_quantity
        else:
            cart[product_id] = {'quantity': quantity}
            
        request.session.modified = True
        messages.success(request, f"{product.name} added to your cart!")
        
        return redirect('cart')
    
    return redirect('collections')

def update_cart(request):
    """Update quantity of an item in the cart"""
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity < 1:
            messages.error(request, "Quantity must be at least 1")
            return redirect('cart')
            
        # Get the product to check stock
        product = get_object_or_404(Product, id=product_id)
        
        # Check if product has enough stock
        if product.stock < quantity:
            messages.error(request, f"Sorry, we only have {product.stock} of this item in stock.")
            return redirect('cart')
            
        # Update cart if it exists
        if 'cart' in request.session:
            cart = request.session['cart']
            if product_id in cart:
                cart[product_id]['quantity'] = quantity
                request.session.modified = True
                messages.success(request, "Cart updated successfully!")
            
        return redirect('cart')
    
    return redirect('collections')

def remove_from_cart(request):
    """Remove an item from the cart"""
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        
        if 'cart' in request.session:
            cart = request.session['cart']
            if product_id in cart:
                product = get_object_or_404(Product, id=product_id)
                del cart[product_id]
                request.session.modified = True
                messages.success(request, f"{product.name} removed from your cart!")
                
        return redirect('cart')
    
    return redirect('collections')
