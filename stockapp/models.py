from django.db import models
from salesapp.models import Product


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateField(auto_now_add=True)
    is_paid = models.BooleanField(default=True)

    class Meta:
        permissions = [
            ("can_manage_stock", "can manage stock"),
            ("can_view_reports", "can view reports"),
        ]

    def save(self, *args, **kwargs):
        self.amount_due = self.quantity * self.unit_cost 
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.product) 