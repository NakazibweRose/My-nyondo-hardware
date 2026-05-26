from django.db import models
from salesapp.models import Product


# Create your models here.
class Stock(models.Model):
    # STOCK_TYPES = [
    #     ('cement', 'Cement'),
    #     ('iron_bars', 'iron_bars'),
    #     ('nails', 'nails'),
    #     ('roofings', 'roofings'),
    #     ('wheelbarrows', 'wheelbarrows'),
    #     ('wire mesh', 'wire mesh'),
    #     ('barbed wire', 'barbed wire'),
        
    # ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.CharField(max_length=100)
    quantity = models.IntegerField( default=0)
    unit_cost = models.IntegerField( default=0)
    amount_paid = models.IntegerField( default=0)
    selling_price = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    is_paid = models.BooleanField(default=True)


    class Meta:
        permissions =[
            ("can_manage_stock", "can manage stock"),
            ("can_view_reports", "can view reports"),
        ]
   
    

    def save(self, *args, **kwargs):
        self.amount_due = self.quantity * self.unit_cost


        super().save(*args, **kwargs)

    def __str__(self):
        return self.product