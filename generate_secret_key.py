#!/usr/bin/env python
"""
Django SECRET_KEY generator.
"""
import random
import string

def generate_secret_key(length=50):
    """
    Generate a secure random string of letters, digits, and special characters
    for use as a SECRET_KEY setting.
    """
    chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(random.SystemRandom().choice(chars) for _ in range(length))

if __name__ == '__main__':
    # Generate a SECRET_KEY
    secret_key = generate_secret_key()
    
    # Print the SECRET_KEY
    print("\nGenerated Django SECRET_KEY:")
    print("-" * 60)
    print(f"SECRET_KEY={secret_key}")
    print("-" * 60)
    
    # Instructions
    print("\nCopy this line to your .env file.")
    print("Remember to never share your SECRET_KEY or commit it to version control!\n") 