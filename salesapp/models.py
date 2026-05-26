from django.db import models
# from stockapp.models import Stock


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.category_name
    

class Customer(models.Model):

    CUSTOMER_TYPES = [
        ("Wholesaler", "Wholesaler"),
        ("Retailer", "Retailer"),
        ("Walk-in", "Walk-in"),
    ]

    full_name = models.CharField(max_length=100 ,null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    customer_type = models.CharField(max_length=20,choices=CUSTOMER_TYPES)

    def __str__(self):
        return self.full_name



class Product(models.Model):
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.product_name


class Sales(models.Model):
    customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=100, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)

    distance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transport_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transport_note = models.TextField(default="", blank=True)

    class Meta:
       permissions = [
           ("can_record_sales", "Can record sales"),
           ("can_issue_receipts", "Can issue receipts"),
       ]


    def __str__(self):
        return f"{self.product_name.product_name} - {self.quantity} "
    

