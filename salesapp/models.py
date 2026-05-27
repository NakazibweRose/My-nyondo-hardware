from django.db import models
# from stockapp.models import Stock


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.product_name


class Sales(models.Model):
    CUSTOMER_TYPES = [
        ('wholesale', 'Wholesale'),
        ('retail', 'Retail'),
        ('walk_in', 'Walk_in')
    ]
    customer_type = models.CharField(max_length=20, choices = CUSTOMER_TYPES, default =" retail")
    customer_name = models.CharField(max_length=30)
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=100, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)

    distance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transport_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transport_note = models.TextField(default="", blank=True)

    def __str__(self):
        return f"{self.product_name.product_name} - {self.quantity} "
    

