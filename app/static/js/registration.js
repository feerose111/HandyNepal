document.getElementById('registrationForm').addEventListener('submit', function(e) {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const passwordError = document.getElementById('passwordError');
    
    if (password !== confirmPassword) {
        e.preventDefault();
        passwordError.textContent = 'Passwords do not match';
        return;
    }
    
    passwordError.textContent = '';
});

document.getElementById('registrationForm').addEventListener('submit', function(e) {
    const email = document.getElementById('email').value;
    const emailError = document.getElementById('emailError');

    if (!isValidEmail(email)) {
        e.preventDefault();
        emailError.textContent = 'Invalid email address';
        return;
    }

    emailError.textContent = '';
});


