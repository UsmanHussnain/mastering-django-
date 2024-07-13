from django.db import models
from . product import Product
from .customer import Customer



class Order(models.Model):


    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(null=True, blank=True)
    def __str__(self):
        return f"{self.customer.first_name}  {self.customer.last_name}"
    
    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer_id=customer_id).order_by('-date')
