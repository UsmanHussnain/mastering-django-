from django.db import models
from .category import Category

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100, blank=True, null= True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null= True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, blank=True, null= True)
    description = models.TextField(blank=True, null= True)
    image = models.ImageField(upload_to='uploads/products', blank=True, null= True)

    def __str__(self):
        return self.name
    
    @staticmethod
    def get_all_products():
        return Product.objects.all()
    
    @staticmethod
    def get_product_by_id(ids):
        return Product.objects.filter(id__in = ids)
    
    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(Category = category_id)
        else:
            return Product.objects.all()