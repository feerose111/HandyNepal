/**
 * HandyNepal Collections Page JavaScript
 * This file handles all the functionality for the collections/product listing page
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize cart from localStorage
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    updateCartCount();
    
    // Product Filtering
    const productItems = document.querySelectorAll('.product-item');
    const categoryFilters = document.querySelectorAll('.category-filter');
    const artisanFilters = document.querySelectorAll('.artisan-filter');
    const priceRange = document.getElementById('priceRange');
    const priceMin = document.getElementById('priceMin');
    const priceMax = document.getElementById('priceMax');
    const applyFiltersBtn = document.getElementById('applyFilters');
    const clearFiltersBtn = document.getElementById('clearFilters');
    const productCount = document.getElementById('productCount');
    const sortSelect = document.getElementById('sortSelect');
    
    // Set initial price range value
    if (priceRange) {
        priceRange.value = 200;
    }
    
    // Initialize product count
    updateProductCount();
    
    // Apply Filters Button Click
    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', function() {
            applyFilters(true);
        });
    }
    
    // Clear Filters Button Click
    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', function() {
            clearFilters();
        });
    }
    
    // Price Range Input Change
    if (priceRange) {
        priceRange.addEventListener('input', function() {
            priceMax.textContent = '$' + this.value;
            // Apply filters in real-time as the price range changes
            applyFilters();
        });
    }
    
    // Category Filter Change
    categoryFilters.forEach(filter => {
        filter.addEventListener('change', function() {
            applyFilters();
        });
    });
    
    // Artisan Filter Change
    artisanFilters.forEach(filter => {
        filter.addEventListener('change', function() {
            applyFilters();
        });
    });
    
    // Sort Select Change
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            sortProducts(this.value);
        });
    }
    
    // Function to update product count
    function updateProductCount() {
        if (productCount) {
            const visibleProducts = Array.from(productItems).filter(item => 
                item.style.display !== 'none'
            );
            productCount.textContent = visibleProducts.length;
        }
    }
    
    // Function to apply filters
    function applyFilters(reloadProducts = false) {
        let selectedCategories = [];
        let selectedArtisans = [];
        let maxPrice = priceRange ? parseFloat(priceRange.value) : 200;
        
        // Get selected categories
        categoryFilters.forEach(filter => {
            if (filter.checked) {
                selectedCategories.push(filter.value);
            }
        });
        
        // Get selected artisans
        artisanFilters.forEach(filter => {
            if (filter.checked) {
                selectedArtisans.push(filter.value);
            }
        });
        
        if (reloadProducts) {
            // Fetch products from server with filters
            fetchFilteredProducts(selectedCategories, selectedArtisans, maxPrice, sortSelect ? sortSelect.value : 'featured');
        } else {
            // Filter products client-side
            let visibleCount = 0;
            
            productItems.forEach(item => {
                const category = item.dataset.category;
                const artisan = item.dataset.artisan;
                const price = parseFloat(item.dataset.price);
                
                const categoryMatch = selectedCategories.length === 0 || selectedCategories.includes(category);
                const artisanMatch = selectedArtisans.length === 0 || selectedArtisans.includes(artisan);
                const priceMatch = price <= maxPrice;
                
                if (categoryMatch && artisanMatch && priceMatch) {
                    item.style.display = '';
                    visibleCount++;
                } else {
                    item.style.display = 'none';
                }
            });
            
            // Update product count
            if (productCount) {
                productCount.textContent = visibleCount;
            }
        }
        
        // Update URL with filter parameters (without page reload)
        updateUrlWithFilters(selectedCategories, selectedArtisans, maxPrice);
    }
    
    // Function to fetch filtered products from server
    function fetchFilteredProducts(categories, artisans, maxPrice, sortBy) {
        // Show loading indicator
        const productGrid = document.getElementById('productGrid');
        productGrid.innerHTML = '<div class="col-12 text-center py-5"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
        
        // Build URL with filter parameters
        const url = new URL(window.location.pathname, window.location.origin);
        const params = url.searchParams;
        
        // Add filter parameters
        if (categories.length > 0) {
            categories.forEach(category => {
                params.append('category', category);
            });
        }
        
        if (artisans.length > 0) {
            artisans.forEach(artisan => {
                params.append('artisan', artisan);
            });
        }
        
        if (maxPrice < 200) {
            params.set('max_price', maxPrice);
        }
        
        if (sortBy && sortBy !== 'featured') {
            params.set('sort_by', sortBy);
        }
        
        // Reset to page 1 when applying new filters
        params.set('page', 1);
        
        // Navigate to the URL with filters
        window.location.href = url.toString();
    }
    
    // Function to initialize event listeners for product items
    function initializeProductEventListeners() {
        // Update product items reference
        const newProductItems = document.querySelectorAll('.product-item');
        
        // Add to Cart Button Click
        const newAddToCartButtons = document.querySelectorAll('.add-to-cart-btn');
        newAddToCartButtons.forEach(button => {
            button.addEventListener('click', function() {
                const productId = this.dataset.productId;
                const productName = this.dataset.productName;
                const productPrice = parseFloat(this.dataset.productPrice);
                
                addToCart(productId, productName, productPrice);
            });
        });
        
        // Quick View Button Click
        const newQuickViewButtons = document.querySelectorAll('.btn-quickview');
        newQuickViewButtons.forEach(button => {
            button.addEventListener('click', function() {
                const productId = this.dataset.productId;
                openQuickView(productId);
            });
        });
        
        // Wishlist Button Click
        const newWishlistButtons = document.querySelectorAll('.btn-wishlist');
        newWishlistButtons.forEach(button => {
            button.addEventListener('click', function() {
                const productId = this.dataset.productId;
                toggleWishlist(productId, this);
            });
        });
        
        // Initialize wishlist
        initWishlist();
    }
    
    // Function to update URL with filter parameters
    function updateUrlWithFilters(categories, artisans, maxPrice) {
        const url = new URL(window.location.href);
        const params = url.searchParams;
        
        // Clear existing filter parameters
        params.delete('category');
        params.delete('artisan');
        params.delete('max_price');
        params.delete('sort_by');
        
        // Add new filter parameters
        if (categories.length > 0) {
            categories.forEach(category => {
                params.append('category', category);
            });
        }
        
        if (artisans.length > 0) {
            artisans.forEach(artisan => {
                params.append('artisan', artisan);
            });
        }
        
        if (maxPrice < 200) {
            params.set('max_price', maxPrice);
        }
        
        if (sortSelect && sortSelect.value !== 'featured') {
            params.set('sort_by', sortSelect.value);
        }
        
        // Preserve page parameter if it exists
        const currentPage = params.get('page');
        if (currentPage) {
            params.set('page', currentPage);
        }
        
        // Update URL without reloading the page
        window.history.replaceState({}, '', url);
    }
    
    // Function to load filters from URL on page load
    function loadFiltersFromUrl() {
        const url = new URL(window.location.href);
        const params = url.searchParams;
        
        // Load categories
        const categories = params.getAll('category');
        if (categories.length > 0) {
            categoryFilters.forEach(filter => {
                if (categories.includes(filter.value)) {
                    filter.checked = true;
                }
            });
        }
        
        // Load artisans
        const artisans = params.getAll('artisan');
        if (artisans.length > 0) {
            artisanFilters.forEach(filter => {
                if (artisans.includes(filter.value)) {
                    filter.checked = true;
                }
            });
        }
        
        // Load max price
        const maxPrice = params.get('max_price');
        if (maxPrice && priceRange) {
            priceRange.value = maxPrice;
            priceMax.textContent = '$' + maxPrice;
        }
        
        // Load sort
        const sortBy = params.get('sort_by');
        if (sortBy && sortSelect) {
            sortSelect.value = sortBy;
        }
        
        // Apply filters
        if (categories.length > 0 || artisans.length > 0 || maxPrice || sortBy) {
            applyFilters();
        }
    }
    
    // Load filters from URL on page load
    loadFiltersFromUrl();
    
    // Function to clear filters
    function clearFilters() {
        // Uncheck all category filters
        categoryFilters.forEach(filter => {
            filter.checked = false;
        });
        
        // Uncheck all artisan filters
        artisanFilters.forEach(filter => {
            filter.checked = false;
        });
        
        // Reset price range
        if (priceRange) {
            priceRange.value = 200;
            priceMax.textContent = '$200';
        }
        
        // Reset sort select
        if (sortSelect) {
            sortSelect.value = 'featured';
        }
        
        // Show all products
        productItems.forEach(item => {
            item.style.display = '';
        });
        
        // Update product count
        updateProductCount();
        
        // Clear URL parameters
        window.history.replaceState({}, '', window.location.pathname);
    }
    
    // Function to sort products
    function sortProducts(sortBy) {
        const productGrid = document.getElementById('productGrid');
        const products = Array.from(productItems);
        
        products.sort((a, b) => {
            const priceA = parseFloat(a.dataset.price);
            const priceB = parseFloat(b.dataset.price);
            
            switch (sortBy) {
                case 'price-low':
                    return priceA - priceB;
                case 'price-high':
                    return priceB - priceA;
                case 'newest':
                    // Sort by data-created attribute if available, otherwise use default
                    if (a.dataset.created && b.dataset.created) {
                        return new Date(b.dataset.created) - new Date(a.dataset.created);
                    }
                    return -1;
                case 'bestselling':
                    // Sort by bestseller flag if available
                    const aIsBestseller = a.dataset.bestseller === 'True';
                    const bIsBestseller = b.dataset.bestseller === 'True';
                    if (aIsBestseller && !bIsBestseller) return -1;
                    if (!aIsBestseller && bIsBestseller) return 1;
                    return 0;
                default:
                    // Featured - use is_featured flag if available
                    const aIsFeatured = a.dataset.featured === 'True';
                    const bIsFeatured = b.dataset.featured === 'True';
                    if (aIsFeatured && !bIsFeatured) return -1;
                    if (!aIsFeatured && bIsFeatured) return 1;
                    return 0;
            }
        });
        
        // Reorder products in the DOM
        products.forEach(product => {
            productGrid.appendChild(product);
        });
        
        // Apply current filters after sorting
        applyFilters();
    }
    
    // Add to Cart Button Click
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            const productName = this.dataset.productName;
            const productPrice = parseFloat(this.dataset.productPrice);
            
            addToCart(productId, productName, productPrice);
        });
    });
    
    // Quick View Button Click
    const quickViewButtons = document.querySelectorAll('.btn-quickview');
    quickViewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            openQuickView(productId);
        });
    });
    
    // Wishlist Button Click
    const wishlistButtons = document.querySelectorAll('.btn-wishlist');
    wishlistButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            toggleWishlist(productId, this);
        });
    });
    
    // Quick View Modal Quantity Buttons
    function setupQuantityButtons() {
        const decreaseQuantityBtn = document.getElementById('decreaseQuantity');
        const increaseQuantityBtn = document.getElementById('increaseQuantity');
        const quantityInput = document.getElementById('quickViewQuantity');
        
        if (decreaseQuantityBtn && increaseQuantityBtn && quantityInput) {
            // Clear any existing event listeners
            const newDecreaseBtn = decreaseQuantityBtn.cloneNode(true);
            const newIncreaseBtn = increaseQuantityBtn.cloneNode(true);
            const newQuantityInput = quantityInput.cloneNode(true);
            
            decreaseQuantityBtn.parentNode.replaceChild(newDecreaseBtn, decreaseQuantityBtn);
            increaseQuantityBtn.parentNode.replaceChild(newIncreaseBtn, increaseQuantityBtn);
            quantityInput.parentNode.replaceChild(newQuantityInput, quantityInput);
            
            // Add event listeners to the new elements
            newDecreaseBtn.addEventListener('click', function() {
                let value = parseInt(newQuantityInput.value);
                if (value > 1) {
                    newQuantityInput.value = value - 1;
                }
            });
            
            newIncreaseBtn.addEventListener('click', function() {
                let value = parseInt(newQuantityInput.value);
                newQuantityInput.value = value + 1;
            });
            
            // Ensure the quantity input only accepts numbers and has a minimum value of 1
            newQuantityInput.addEventListener('input', function() {
                let value = this.value;
                // Remove non-numeric characters
                value = value.replace(/[^0-9]/g, '');
                // Ensure minimum value is 1
                value = value === '' ? 1 : Math.max(1, parseInt(value));
                this.value = value;
            });
            
            // Prevent manual input of invalid values
            newQuantityInput.addEventListener('blur', function() {
                if (this.value === '' || isNaN(parseInt(this.value))) {
                    this.value = 1;
                }
            });
            
            // Prevent the default behavior of the up/down arrows to avoid conflicts
            newQuantityInput.addEventListener('keydown', function(e) {
                if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    let value = parseInt(this.value);
                    this.value = value + 1;
                } else if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    let value = parseInt(this.value);
                    if (value > 1) {
                        this.value = value - 1;
                    }
                }
            });
        }
    }
    
    // Function to open quick view modal
    function openQuickView(productId) {
        const quickViewModal = document.getElementById('quickViewModal');
        const quickViewTitle = document.getElementById('quickViewTitle');
        const quickViewPrice = document.getElementById('quickViewPrice');
        const quickViewDescription = document.getElementById('quickViewDescription');
        const quickViewImage = document.getElementById('quickViewImage');
        const quickViewAddToCart = document.getElementById('quickViewAddToCart');
        const quickViewStock = document.getElementById('quickViewStock');
        const quickViewArtisan = document.getElementById('quickViewArtisan');
        const quickViewQuantity = document.getElementById('quickViewQuantity');
        
        // Get product data from hidden div
        const productData = document.getElementById(`product-data-${productId}`);
        
        if (!productData) {
            console.error(`Product data not found for product ID: ${productId}`);
            showMessage('Error loading product details. Please try again.', 'danger');
            return;
        }
        
        // Try to find the product card and image
        let productImage = '';
        const productCardElement = document.querySelector(`[data-product-id="${productId}"]`);
        
        if (productCardElement) {
            const productCard = productCardElement.closest('.product-card');
            if (productCard && productCard.querySelector('img')) {
                productImage = productCard.querySelector('img').src;
            }
        }
        
        // If we couldn't find the image, use a placeholder
        if (!productImage) {
            productImage = '/static/images/product.png';
        }
        
        // Set modal content from data attributes
        quickViewTitle.textContent = productData.dataset.name;
        
        // Set price with discount if available
        if (productData.dataset.isDiscount === 'True') {
            quickViewPrice.innerHTML = `<span class="original-price">$${productData.dataset.price}</span> $${productData.dataset.discountPrice}`;
        } else {
            quickViewPrice.innerHTML = `$${productData.dataset.price}`;
        }
        
        quickViewDescription.textContent = productData.dataset.description;
        quickViewImage.src = productImage;
        
        // Show stock information
        const stockCount = parseInt(productData.dataset.stock);
        if (stockCount > 10) {
            quickViewStock.innerHTML = `<i class="fas fa-check-circle text-success"></i> In Stock (${stockCount} available)`;
        } else if (stockCount > 0) {
            quickViewStock.innerHTML = `<i class="fas fa-exclamation-circle text-warning"></i> Low Stock (Only ${stockCount} left)`;
        } else {
            quickViewStock.innerHTML = `<i class="fas fa-times-circle text-danger"></i> Out of Stock`;
        }
        
        // Show artisan information if available
        if (productData.dataset.artisan) {
            quickViewArtisan.innerHTML = `<small class="text-muted">Crafted by: ${productData.dataset.artisan} (${productData.dataset.artisanType})</small>`;
        } else {
            quickViewArtisan.innerHTML = '';
        }
        
        // Set the product ID and price for the Add to Cart button
        quickViewAddToCart.setAttribute('data-product-id', productId);
        quickViewAddToCart.setAttribute('data-product-name', productData.dataset.name);
        
        // Set the correct price (discounted or regular)
        const priceForCart = productData.dataset.isDiscount === 'True' ? 
            productData.dataset.discountPrice : productData.dataset.price;
        quickViewAddToCart.setAttribute('data-product-price', priceForCart);
        
        // Reset quantity
        if (quickViewQuantity) {
            quickViewQuantity.value = 1;
        }
        
        // Setup quantity buttons
        setupQuantityButtons();
        
        // Setup Add to Cart button
        setupQuickViewAddToCart();
        
        // Setup Add to Wishlist button
        setupQuickViewAddToWishlist();
        
        // Show the modal
        const modal = new bootstrap.Modal(quickViewModal);
        modal.show();
    }
    
    // Setup Quick View Add to Cart Button
    function setupQuickViewAddToCart() {
        const quickViewAddToCartBtn = document.getElementById('quickViewAddToCart');
        if (quickViewAddToCartBtn) {
            // Remove existing event listeners
            const newBtn = quickViewAddToCartBtn.cloneNode(true);
            quickViewAddToCartBtn.parentNode.replaceChild(newBtn, quickViewAddToCartBtn);
            
            // Add new event listener
            newBtn.addEventListener('click', function() {
                const productId = this.dataset.productId;
                const productName = this.dataset.productName;
                const productPrice = parseFloat(this.dataset.productPrice);
                const quantity = parseInt(document.getElementById('quickViewQuantity').value) || 1;
                
                addToCart(productId, productName, productPrice, quantity);
                
                // Close modal
                const quickViewModal = bootstrap.Modal.getInstance(document.getElementById('quickViewModal'));
                if (quickViewModal) {
                    quickViewModal.hide();
                }
            });
        }
    }
    
    // Setup Quick View Add to Wishlist Button
    function setupQuickViewAddToWishlist() {
        const quickViewAddToWishlist = document.getElementById('quickViewAddToWishlist');
        const quickViewAddToCartBtn = document.getElementById('quickViewAddToCart');
        
        if (quickViewAddToWishlist && quickViewAddToCartBtn) {
            // Remove existing event listeners
            const newBtn = quickViewAddToWishlist.cloneNode(true);
            quickViewAddToWishlist.parentNode.replaceChild(newBtn, quickViewAddToWishlist);
            
            // Add new event listener
            newBtn.addEventListener('click', function() {
                const productId = quickViewAddToCartBtn.dataset.productId;
                
                // Find the wishlist button for this product
                const wishlistButton = document.querySelector(`.btn-wishlist[data-product-id="${productId}"]`);
                if (wishlistButton) {
                    toggleWishlist(productId, wishlistButton);
                }
                
                // Close the modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('quickViewModal'));
                if (modal) {
                    modal.hide();
                }
            });
        }
    }
    
    // Function to toggle wishlist
    function toggleWishlist(productId, button) {
        // Get wishlist from localStorage
        let wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
        
        // Check if product is already in wishlist
        const index = wishlist.indexOf(productId);
        
        if (index === -1) {
            // Add to wishlist
            wishlist.push(productId);
            button.innerHTML = '<i class="fas fa-heart"></i>';
            button.classList.add('active');
            showMessage('Product added to wishlist', 'success');
        } else {
            // Remove from wishlist
            wishlist.splice(index, 1);
            button.innerHTML = '<i class="far fa-heart"></i>';
            button.classList.remove('active');
            showMessage('Product removed from wishlist', 'info');
        }
        
        // Save wishlist to localStorage
        localStorage.setItem('wishlist', JSON.stringify(wishlist));
    }
    
    // Function to add to cart - Make it globally accessible
    function addToCart(productId, productName, productPrice, quantity = 1) {
        // Check if product already in cart
        const existingItem = cart.find(item => item.id === productId);
        
        if (existingItem) {
            existingItem.quantity += quantity;
        } else {
            cart.push({
                id: productId,
                name: productName,
                price: productPrice,
                quantity: quantity
            });
        }
        
        // Save cart to localStorage
        localStorage.setItem('cart', JSON.stringify(cart));
        
        // Update cart count
        updateCartCount();
        
        // Show success message
        showAddToCartMessage(productName);
        
        // Update cart modal
        updateCartModal();
        
        // Show cart modal
        const cartModal = new bootstrap.Modal(document.getElementById('cartModal'));
        cartModal.show();
    }
    
    // Function to update cart count in navbar
    function updateCartCount() {
        const totalItems = cart.reduce((total, item) => total + item.quantity, 0);
        const cartCountElements = document.querySelectorAll('.cart-count');
        cartCountElements.forEach(element => {
            element.textContent = totalItems;
        });
    }
    
    // Function to show add to cart message
    function showAddToCartMessage(productName) {
        const message = `<div class="alert alert-success alert-dismissible fade show" role="alert">
            <strong>${productName}</strong> has been added to your cart.
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`;
        
        // Add message to page
        document.body.insertAdjacentHTML('beforeend', message);
        
        // Auto remove after 3 seconds
        setTimeout(function() {
            const alert = document.querySelector('.alert');
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 3000);
    }
    
    // Function to show generic message
    function showMessage(message, type = 'info') {
        const messageHtml = `<div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`;
        
        // Add message to page
        document.body.insertAdjacentHTML('beforeend', messageHtml);
        
        // Auto remove after 3 seconds
        setTimeout(function() {
            const alert = document.querySelector('.alert');
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 3000);
    }
    
    // Function to update cart modal
    function updateCartModal() {
        const cartItemsContainer = document.getElementById('cart-items');
        if (!cartItemsContainer) return;
        
        cartItemsContainer.innerHTML = '';
        
        if (cart.length === 0) {
            cartItemsContainer.innerHTML = '<p class="text-center">Your cart is empty</p>';
            document.getElementById('cart-total').textContent = '$0.00';
            return;
        }
        
        let total = 0;
        
        cart.forEach(item => {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;
            
            const itemHtml = `
                <div class="cart-item d-flex justify-content-between align-items-center mb-3">
                    <div>
                        <h6 class="mb-0">${item.name}</h6>
                        <small class="text-muted">$${item.price.toFixed(2)} x ${item.quantity}</small>
                    </div>
                    <div class="d-flex align-items-center">
                        <span class="me-3">$${itemTotal.toFixed(2)}</span>
                        <button class="btn btn-sm btn-outline-danger remove-item" data-product-id="${item.id}">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </div>
                </div>
            `;
            
            cartItemsContainer.insertAdjacentHTML('beforeend', itemHtml);
        });
        
        document.getElementById('cart-total').textContent = '$' + total.toFixed(2);
        
        // Add event listeners for remove buttons
        document.querySelectorAll('.remove-item').forEach(button => {
            button.addEventListener('click', function() {
                const productId = this.dataset.productId;
                removeFromCart(productId);
            });
        });
    }
    
    // Function to remove item from cart
    function removeFromCart(productId) {
        cart = cart.filter(item => item.id !== productId);
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartCount();
        updateCartModal();
    }
    
    // Initialize - check if products are in wishlist
    function initWishlist() {
        const wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
        
        wishlistButtons.forEach(button => {
            const productId = button.dataset.productId;
            if (wishlist.includes(productId)) {
                button.innerHTML = '<i class="fas fa-heart"></i>';
                button.classList.add('active');
            }
        });
    }
    
    // Initialize wishlist
    initWishlist();
    
    // Handle pagination with AJAX
    function initPaginationLinks() {
        const paginationLinks = document.querySelectorAll('.pagination .page-link:not([aria-disabled="true"])');
        
        paginationLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Get the URL from the link
                const url = this.href;
                
                // Show loading indicator
                const productGrid = document.getElementById('productGrid');
                productGrid.innerHTML = '<div class="col-12 text-center py-5"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
                
                // Make a full page request (not AJAX) to get the complete HTML
                window.location.href = url;
            });
        });
    }
    
    // Initialize pagination links
    initPaginationLinks();
}); 