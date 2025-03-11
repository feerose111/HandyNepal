from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('artisan', 'Artisan'),
    )
    
    full_name = models.CharField(max_length=255)
    
    # Email and password are already part of AbstractUser
    
    phone_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    
    # Override the groups and user_permissions fields to add related_name
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='app_user_set',  # Custom related_name to avoid clash
        related_query_name='app_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='app_user_set',  # Custom related_name to avoid clash
        related_query_name='app_user',
    )
    
    def __str__(self):
        return self.full_name or self.username
    
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    isDelete = models.BooleanField(default=False)
    deleted_time = models.DateTimeField(null=True, blank=True)

