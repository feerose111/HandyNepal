// Add auto-dismiss functionality for alert messages
document.addEventListener('DOMContentLoaded', function() {
    // Get all alert elements
    const alerts = document.querySelectorAll('.alert');
    
    // Auto dismiss alerts after 5 seconds
    alerts.forEach(alert => {
        setTimeout(() => {
            // Add fade-out animation
            alert.classList.add('fade-out');
            
            // Remove the alert after animation completes
            setTimeout(() => {
                alert.remove();
            }, 500); // Match this to the animation duration
        }, 5000); // 5 seconds before starting to fade out
    });
    
    // Allow manual dismissal with close button
    const closeButtons = document.querySelectorAll('.alert .btn-close');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const alert = this.closest('.alert');
            alert.classList.add('fade-out');
            
            setTimeout(() => {
                alert.remove();
            }, 500);
        });
    });
});

// Existing JavaScript code continues below 