from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import datetime
from base.constant import GENDER_CHOICES, PROVINCE_CHOICES, PAYMENT_METHOD_CHOICES, ORDER_CHOICES


class customuser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    father_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES)
    city = models.CharField(max_length=50)
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20)
    about = models.TextField(max_length=500)
    profile_pic = models.ImageField(upload_to='profile_pic/', null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email
    

    
    def generate_verification_token(self):
        token = get_random_string(length=32)
        self.verification_token = token
        self.save()
        return token

    def send_email_verification(self):
        subject = 'Verify Your Email Address'
        token = self.generate_verification_token()
        message = f'Hi {self.first_name},\n\nPlease click the link below to verify your email address:\n\n' \
                  f'{settings.BASE_URL}/verify-email/{token}/\n\nThank you!'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [self.email])

@receiver(pre_delete, sender=customuser)
def delete_user_image(sender, instance, **kwargs):
    if instance.profile_pic:
        instance.profile_pic.delete(save=False)


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



    

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_quantity = models.PositiveIntegerField()
    available_quantity = models.PositiveIntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return self.name
    
    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in = ids)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Image of {self.product.name}"
    
    
    

class Order(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    shipping_first_name = models.CharField(max_length=255, blank=True, null=True)
    shipping_last_name = models.CharField(max_length=255, blank=True, null=True)
    shipping_email = models.EmailField(blank=True, null=True)
    shipping_phone = models.CharField(max_length=20, blank=True, null=True)
    shipping_address = models.CharField(max_length=255, blank=True, null=True)
    shipping_country = models.CharField(max_length=255, blank=True, null=True)
    shipping_city = models.CharField(max_length=255, blank=True, null=True)
    shipping_state = models.CharField(max_length=255, blank=True, null=True)
    shipping_zip_code = models.CharField(max_length=10, blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_CHOICES, default='Pending', blank=True, null=True)
    user = models.ForeignKey(customuser, on_delete=models.CASCADE, related_name='orders', null=False)


    def __str__(self):
        return f"Order {self.id} by {self.user.email if self.user else 'Unknown'}"
    @property
    def total_price(self):
        return sum(item.total_price for item in self.orderitem_set.all())    
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    user = models.ForeignKey(customuser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity}) for Order {self.order.id} by {self.order.user.email if self.order.user else 'Unknown'}"



class CustomerReview(models.Model):
    user = models.ForeignKey(customuser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    profession = models.CharField(max_length=255)
    review = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review by {self.user.first_name} {self.user.last_name} for {self.product.name}"
    
    
    
class Querries(models.Model):
    user = models.ForeignKey(customuser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(max_length=500)
    
    def __str__(self):
        return f"Query by {self.user.first_name} {self.user.last_name}"