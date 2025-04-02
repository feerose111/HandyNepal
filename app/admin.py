from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Artisan)
admin.site.register(OrderDetail)

@admin.register(PaymentDetails)
class PaymentDetailsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'full_name', 'amount', 'payment_method', 'payment_status', 'payment_date')
    list_filter = ('payment_status', 'payment_method', 'payment_date')
    search_fields = ('full_name', 'email', 'phone', 'transaction_id', 'purchase_order_id')
    readonly_fields = ('payment_date',)
    fieldsets = (
        ('Payment Information', {
            'fields': ('user', 'transaction_id', 'purchase_order_id', 'amount', 'payment_status', 'payment_method', 'payment_date')
        }),
        ('Customer Information', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Address Information', {
            'fields': ('address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Additional Information', {
            'fields': ('terms_accepted', 'notes')
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        # Prevent accidental deletion of payment records
        return True

