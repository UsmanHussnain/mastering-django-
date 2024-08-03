from django.contrib import admin
from .models import customuser, Product, Brand, Category, ProductImage, Order, OrderItem, CustomerReview, Querries
# Register your models here.


@admin.register(customuser)
class customuserAdmin(admin.ModelAdmin):
   
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active']
    
try:
    admin.site.unregister(Order)
except admin.sites.NotRegistered:
    pass

    
    
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user_email', 'first_name', 'last_name', 'email', 'phone', 'address', 'payment_method')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'address', 'payment_method')
    
    def get_user_email(self, obj):
        return obj.user.email if obj.user else 'Unknown'
    
    get_user_email.short_description = 'User Email'

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'user')
    
    

admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(CustomerReview)
admin.site.register(Querries)
