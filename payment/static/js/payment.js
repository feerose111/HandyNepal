document.addEventListener('DOMContentLoaded', function() {
    // Load cart items from localStorage
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const orderItems = document.getElementById('order-items');
    const orderTotal = document.getElementById('order-total');
    
    // Display order items
    if (cart.length > 0) {
        let total = 0;
        cart.forEach(item => {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;
            
            const itemHtml = `
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <div>
                        <h6 class="mb-0">${item.name}</h6>
                        <small class="text-muted">$${item.price.toFixed(2)} x ${item.quantity}</small>
                    </div>
                    <span>$${itemTotal.toFixed(2)}</span>
                </div>
            `;
            
            orderItems.insertAdjacentHTML('beforeend', itemHtml);
        });
        
        orderTotal.textContent = `$${total.toFixed(2)}`;
    } else {
        orderItems.innerHTML = '<p class="text-center">No items in cart</p>';
        orderTotal.textContent = '$0.00';
    }
    
    // Format card number input
    const cardNumber = document.getElementById('cardNumber');
    if (cardNumber) {
        cardNumber.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.replace(/(\d{4})/g, '$1 ').trim();
            e.target.value = value;
        });
    }
    
    // Format expiry date input
    const expiryDate = document.getElementById('expiryDate');
    if (expiryDate) {
        expiryDate.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length >= 2) {
                value = value.slice(0, 2) + '/' + value.slice(2);
            }
            e.target.value = value;
        });
    }
    
    // Format CVV input
    const cvv = document.getElementById('cvv');
    if (cvv) {
        cvv.addEventListener('input', function(e) {
            e.target.value = e.target.value.replace(/\D/g, '').slice(0, 4);
        });
    }
    
    // Handle form submission
    const paymentForm = document.getElementById('payment-form');
    if (paymentForm) {
        paymentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Here you would typically:
            // 1. Validate the form data
            // 2. Send the payment information to your payment processor
            // 3. Handle the response
            
            // For now, we'll just show a success message
            alert('Payment successful! Thank you for your purchase.');
            
            // Clear the cart
            localStorage.removeItem('cart');
            
            // Redirect to home page
            window.location.href = '/';
        });
    }
}); 