import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpRequest , HttpResponse
from datetime import datetime
from django.utils import timezone
from .models import User, Contact, Artisan, Product, PaymentDetails# Import the custom User model and Order models
from django.core.paginator import Paginator
import uuid
import json, requests
from django.conf import settings
from decimal import Decimal

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
    context = {}
    
    # Add current date to context
    context['current_date'] = timezone.now().strftime("%B %d, %Y")
    
    # For buyer dashboard
    if request.user.role == 'buyer':
        # Get payment details for this user
        payment_details = PaymentDetails.objects.filter(email=request.user.email).order_by('-payment_date')
        
        # Count payment statuses
        pending_orders_count = payment_details.filter(payment_status='Pending').count()
        completed_orders_count = payment_details.filter(payment_status='Completed').count()
        
        # Get recent payments for order display
        pending_orders = payment_details.filter(payment_status='Pending')
        completed_orders = payment_details.filter(payment_status='Completed')
        recent_orders = payment_details.order_by('-payment_date')[:5]
        
        # Calculate days since user registration
        days_active = (timezone.now() - request.user.date_joined).days
        
        # Create recent activities from payment history
        recent_activities = []
        for payment in payment_details[:5]:
            icon = 'fas fa-shopping-cart'
            if payment.payment_status == 'Completed':
                description = f"Payment of ₹{payment.amount} completed"
                icon = 'fas fa-check-circle'
            elif payment.payment_status == 'Pending':
                description = f"Payment of ₹{payment.amount} pending"
                icon = 'fas fa-clock'
            elif payment.payment_status in ['Refunded', 'Expired', 'User canceled']:
                description = f"Payment of ₹{payment.amount} {payment.payment_status.lower()}"
                icon = 'fas fa-times-circle'
            else:
                description = f"Order placed for ₹{payment.amount}"
            
            recent_activities.append({
                'icon': icon,
                'description': description,
                'timestamp': payment.payment_date.strftime("%B %d, %Y, %I:%M %p")
            })
        
        # Add data to context
        context.update({
            'pending_orders_count': pending_orders_count,
            'completed_orders_count': completed_orders_count,
            'pending_orders': pending_orders,
            'completed_orders': completed_orders,
            'recent_orders': recent_orders,
            'days_active': days_active,
            'recent_activities': recent_activities,
        })
    
    return render(request, 'main/dashboard.html', context)

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

    
    if request.method == "POST":
        amount = request.POST.get('amount')
        amount = int(amount)
        amount_in_rupee = int(amount/100) #changing back to rupees
        purchase_order_id = request.POST.get('purchase_order_id')
        return_url = request.POST.get('return_url')
        website_url = request.POST.get('return_url')
        
        #customer information
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        #added info
        terms_accepted = request.POST.get('terms_accepted') == 'on'
    
        PaymentDetails.objects.get_or_create(amount = amount_in_rupee , purchase_order_id = purchase_order_id,
                        full_name = full_name, email = email, phone = phone, address = address, terms_accepted = terms_accepted)

        payload = json.dumps({
            "return_url": return_url,
            "website_url": website_url,
            "amount": amount,
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": "test",
            "customer_info": {
            "name": full_name,
            "email": email,
            "phone": phone
            }
        })
        
        headers = {
            'Authorization': LIVE_SECRET_KEY,
            'Content-Type': 'application/json',
        }
        
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            response_data = json.loads(response.text)
            
            if 'payment_url' in response_data:
                return redirect(response_data['payment_url'])
            else:
                print(f"Error from Khalti: {response_data}")
                messages.error(request, "Payment initialization failed. Please try again.")
                return redirect('payment_portal')
                
        except Exception as e:
            print(f"Error initializing payment: {str(e)}")
            messages.error(request, "Payment service is currently unavailable. Please try again later.")
            return redirect('payment_portal')
    
    # If not a POST request or other issue
    return redirect('payment_portal')

def verify(request):
    """Verify Khalti payment status using lookup API"""
    if request.method == 'GET':
        # Get parameters from the Khalti callback
        pidx = request.GET.get('pidx')
        transaction_id = request.GET.get('transaction_id')
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
            
            payment_details  = PaymentDetails.objects.get(purchase_order_id = purchase_order_id)
            
            # If payment is complete, process the order
            if lookup_status == 'Completed':
                # Payment successful, process the order
                payment_details.payment_status = lookup_status
                payment_details.transaction_id = transaction_id
                payment_details.save()
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
                payment_details.payment_status = lookup_status
                payment_details.save()
                messages.error(request, f"Payment {lookup_status.lower()}. Please try again.")
                return redirect('cart')
                
            else:
                # Unknown status
                payment_details.payment_status = 'unknown error'
                payment_details.save()
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
