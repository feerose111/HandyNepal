    document.addEventListener('DOMContentLoaded', function() {
        // Make main dashboard tabs work
        const dashboardTabs = document.querySelectorAll('.dashboard-menu a[data-bs-toggle="tab"]');
        dashboardTabs.forEach(tab => {
            tab.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Remove active class from all tabs
                document.querySelectorAll('.dashboard-menu li').forEach(item => {
                    item.classList.remove('active');
                });
                
                // Add active class to clicked tab
                this.parentElement.classList.add('active');
                
                // Get target tab pane
                const target = this.getAttribute('href');
                
                // Hide all tab panes
                document.querySelectorAll('.tab-content > .tab-pane').forEach(pane => {
                    pane.classList.remove('show', 'active');
                });
                
                // Show target tab pane
                document.querySelector(target).classList.add('show', 'active');
            });
        });
        
        // Order status update form handling
        const orderStatusForms = document.querySelectorAll('.order-status-form');
        if (orderStatusForms.length > 0) {
            orderStatusForms.forEach(form => {
                // Add animation when status is changed
                const statusSelect = form.querySelector('select[name="order_status"]');
                if (statusSelect) {
                    statusSelect.addEventListener('change', function() {
                        const submitBtn = form.querySelector('button[type="submit"]');
                        if (submitBtn) {
                            submitBtn.classList.add('btn-pulse');
                            setTimeout(() => {
                                submitBtn.classList.remove('btn-pulse');
                            }, 500);
                        }
                    });
                }
            });
        }
        
        // Make nested tabs work (orders, manage orders)
        const nestedTabs = document.querySelectorAll('.nav-tabs .nav-link[data-bs-toggle="tab"]');
        nestedTabs.forEach(tab => {
            tab.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Remove active class from all tabs in this set
                this.closest('.nav-tabs').querySelectorAll('.nav-link').forEach(link => {
                    link.classList.remove('active');
                });
                
                // Add active class to clicked tab
                this.classList.add('active');
                
                // Get target tab pane
                const target = this.getAttribute('href');
                
                // Find the correct parent tab content that contains these nested panes
                const parentTabContent = this.closest('.tab-content');
                
                // Hide all tab panes in this set
                parentTabContent.querySelectorAll('.tab-pane').forEach(pane => {
                    pane.classList.remove('show', 'active');
                });
                
                // Show target tab pane
                document.querySelector(target).classList.add('show', 'active');
            });
        });

        // Order status filter functionality for order tables
        const orderStatusFilter = document.getElementById('manageOrderStatusFilter');
        if (orderStatusFilter) {
            orderStatusFilter.addEventListener('change', function() {
                const selectedStatus = this.value;
                const orderRows = document.querySelectorAll('#manageOrdersTable .order-row');
                
                orderRows.forEach(row => {
                    if (selectedStatus === 'all' || row.getAttribute('data-status') === selectedStatus) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
                
                // Show "No orders found" message if no visible orders
                const visibleOrders = Array.from(orderRows).filter(row => row.style.display !== 'none');
                const noOrdersRow = document.querySelector('#manageOrdersTable tr:not(.order-row)');
                
                if (visibleOrders.length === 0 && noOrdersRow) {
                    noOrdersRow.style.display = '';
                } else if (noOrdersRow) {
                    noOrdersRow.style.display = 'none';
                }
            });
        }
        
        // Product status filter functionality for seller products
        const productStatusFilter = document.getElementById('productStatusFilter');
        if (productStatusFilter) {
            productStatusFilter.addEventListener('change', function() {
                const selectedStatus = this.value;
                const productRows = document.querySelectorAll('#productsTable .product-row');
                
                productRows.forEach(row => {
                    if (selectedStatus === 'all' || row.getAttribute('data-status') === selectedStatus) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
                
                // Show "No products found" message if no visible products
                const visibleProducts = Array.from(productRows).filter(row => row.style.display !== 'none');
                const noProductsRow = document.querySelector('#productsTable tr:not(.product-row)');
                
                if (visibleProducts.length === 0 && noProductsRow) {
                    noProductsRow.style.display = '';
                } else if (noProductsRow) {
                    noProductsRow.style.display = 'none';
                }
            });
        }
    });

    document.addEventListener('DOMContentLoaded', function() {
        const editProfileBtn = document.getElementById('edit-profile-btn');
        const cancelEditBtn = document.getElementById('cancel-edit-btn');
        const userInfoDisplay = document.getElementById('user-info-display');
        const userInfoForm = document.getElementById('user-info-form');
        
        editProfileBtn.addEventListener('click', function() {
            userInfoDisplay.style.display = 'none';
            userInfoForm.style.display = 'block';
        });
        
        cancelEditBtn.addEventListener('click', function() {
            userInfoForm.style.display = 'none';
            userInfoDisplay.style.display = 'block';
        });
    });
