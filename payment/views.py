from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

# Create your views here.
def payment_portal(request):
    # Get cart data from session or localStorage
    return render(request, 'payment/payment_portal.html')

@require_POST
def process_payment(request):
    try:
        # Get payment data from the form
        payment_data = {
            'firstName': request.POST.get('firstName'),
            'lastName': request.POST.get('lastName'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'address': request.POST.get('address'),
            'paymentType': request.POST.get('paymentType')
        }
        
        # Handle different payment types
        if payment_data['paymentType'] == 'cash':
            # Process cash on delivery order
            # Here you would typically:
            # 1. Create an order in your database
            # 2. Send confirmation emails
            # 3. Update inventory
            
            messages.success(request, 'Your order has been placed successfully! You will pay on delivery.')
            return redirect('home')
            
        elif payment_data['paymentType'] == 'esewa':
            # Process eSewa payment
            # Here you would typically:
            # 1. Create an order in your database
            # 2. Generate eSewa payment parameters
            # 3. Redirect to eSewa payment gateway
            
            # For now, just simulate success
            messages.success(request, 'Your order has been placed successfully! Thank you for your payment.')
            return redirect('home')
        
        else:
            messages.error(request, 'Invalid payment type selected.')
            return redirect('payment:payment_portal')
        
    except Exception as e:
        messages.error(request, f'Order processing failed: {str(e)}')
        return redirect('payment:payment_portal')
