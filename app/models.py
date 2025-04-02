from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from decimal import Decimal

class User(AbstractUser):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller')
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
    
    def __str__(self):
        return self.name
    
class Artisan(models.Model):
    ARTISAN_TYPE_CHOICES = (
        ('textile_weaver', 'Textile Weaver'),
        ('potter', 'Potter'),
        ('woodworker', 'Woodworker'),
        ('metalsmith', 'Metalsmith'),
        ('jewelry_maker', 'Jewelry Maker'),
        ('basket_weaver', 'Basket Weaver'),
        ('leather_worker', 'Leather Worker'),
        ('paper_maker', 'Paper Maker'),
        ('glass_blower', 'Glass Blower'),
        ('other', 'Other'),
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    artisan_type = models.CharField(max_length=50, choices=ARTISAN_TYPE_CHOICES)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='artisans/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True, related_name='artisans')
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    def get_artisan_type_display(self):
        """Return the display name of the artisan type"""
        return dict(self.ARTISAN_TYPE_CHOICES).get(self.artisan_type, '')
    
class Product(models.Model):
    CATEGORY_CHOICES = (
        ('wood-crafts', 'Wood Crafts'),
        ('pottery', 'Pottery'),
        ('textiles', 'Textiles'),
        ('metal-works', 'Metal Works'),
        ('paper-crafts', 'Paper Crafts'),
        ('jewelry', 'Jewelry'),
        ('other', 'Other'),
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    artisan = models.ForeignKey(Artisan, on_delete=models.CASCADE, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    @property
    def get_display_price(self):
        return self.discount_price if self.discount_price else self.price
    
    @property
    def has_discount(self):
        return self.discount_price is not None and self.discount_price < self.price
    
    @property
    def is_discount(self):
        """Alias for has_discount to match template naming"""
        return self.has_discount
    
    @property
    def discount_percentage(self):
        """Calculate discount percentage if there is a discount price"""
        if self.has_discount and self.discount_price is not None:
            discount = ((self.price - self.discount_price) / self.price) * 100
            return int(discount)  # Return as integer for clean display
        return 0
    
    @property
    def get_category_display_name(self):
        """Return the display name of the category"""
        return dict(self.CATEGORY_CHOICES).get(self.category, '')

class PaymentDetails(models.Model):
    """Model for storing payment details along with shipping information"""
    # Payment information
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    purchase_order_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default='pending')
    payment_method = models.CharField(max_length=20, default='khalti')
    
    # Customer information (for guests or to backup user info)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField()
    
    # Additional information
    terms_accepted = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Payment Detail'
        verbose_name_plural = 'Payment Details'
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Payment - {self.full_name} - {self.amount}"
    
class OrderDetail(models.Model):
    ORDER_STATUS_CHOICE = (
        ('processing' , 'Processing'),
        ('shipping', 'Shipping'),
        ('delivered', 'Delivered')
    )
    order_id = models.ForeignKey(PaymentDetails , on_delete= models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order #{self.order_id} - {self.order_status}"
    

