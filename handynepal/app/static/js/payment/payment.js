document.addEventListener('DOMContentLoaded', function() {
    // Load cart items from localStorage
    loadCartItems();
    
    // Set up event listeners
    initEventListeners();
});

/**
 * Load and display cart items from localStorage
 */
function loadCartItems() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const orderItems = document.getElementById('order-items');
    const orderTotal = document.getElementById('order-total');
    
    // Display order items
    if (cart.length > 0) {
        let total = 0;
        let itemsHtml = '';
        
        cart.forEach(item => {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;
            
            itemsHtml += `
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <div>
                        <h6 class="mb-0">${item.name}</h6>
                        <small class="text-muted">$${item.price.toFixed(2)} x ${item.quantity}</small>
                    </div>
                    <span>$${itemTotal.toFixed(2)}</span>
                </div>
            `;
        });
        
        orderItems.innerHTML = itemsHtml;
        orderTotal.textContent = `$${total.toFixed(2)}`;
        
        // Update hidden form fields if they exist
        const amountField = document.getElementById('amount');
        const totalAmountField = document.getElementById('total_amount');
        
        if (amountField) {
            amountField.value = total.toFixed(2);
        }
        
        if (totalAmountField) {
            // Add tax or any other charges if needed
            const taxAmount = parseFloat(document.getElementById('tax_amount')?.value || 0);
            totalAmountField.value = (total + taxAmount).toFixed(2);
        }
    } else {
        orderItems.innerHTML = '<p class="text-center">No items in cart</p>';
        orderTotal.textContent = '$0.00';
    }
}

/**
 * Initialize all event listeners
 */
function initEventListeners() {
    // Payment form submission
    const paymentForm = document.getElementById('payment-form');
    if (paymentForm) {
        paymentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleCashOnDelivery();
        });
    }
}

/**
 * Handle cash on delivery payment method
 */
function handleCashOnDelivery() {
    // Collect form data
    const formData = {
        firstName: document.getElementById('username').value,
        lastName: '',
        email: '',
        phone: '',
        address: document.getElementById('address').value,
        paymentType: 'cash',
        cart: JSON.parse(localStorage.getItem('cart')) || []
    };
    
    // Send order data to server
    fetch('/create-order/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Clear the cart
            localStorage.removeItem('cart');
            
            // Dispatch cart update event
            window.dispatchEvent(new CustomEvent('cartUpdated'));
            
            // Show success message and redirect to home
            alert('Order successfully placed! Your order ID is: ' + data.order_id);
            window.location.href = '/';
        } else {
            alert('There was a problem processing your order: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was a problem processing your order. Please try again later.');
    });
}

/**
 * Get CSRF token from cookies
 */
function getCsrfToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    
    return cookieValue || '';
} 