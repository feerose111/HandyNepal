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
        
        // Make nested tabs work (orders, manage orders)
        const nestedTabs = document.querySelectorAll('.nav-tabs .nav-link[data-bs-toggle="tab"]');
        nestedTabs.forEach(tab => {
            tab.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Find parent tab content
                const parentTabContent = this.closest('.tab-content').parentElement;
                
                // Remove active class from all tabs in this set
                this.closest('.nav-tabs').querySelectorAll('.nav-link').forEach(link => {
                    link.classList.remove('active');
                });
                
                // Add active class to clicked tab
                this.classList.add('active');
                
                // Get target tab pane
                const target = this.getAttribute('href');
                
                // Hide all tab panes in this set
                parentTabContent.querySelectorAll('.tab-pane').forEach(pane => {
                    pane.classList.remove('show', 'active');
                });
                
                // Show target tab pane
                document.querySelector(target).classList.add('show', 'active');
            });
        });
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
