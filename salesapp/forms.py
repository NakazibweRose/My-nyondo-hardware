from django import forms
from .models import Sales
from stockapp.models import Product


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = [
            "customer_type",
            "customer_name",
            "product_name",
            "quantity",
            "distance",
            "transport_required",
        ]

        widgets = {
            "customer_type": forms.Select(attrs={"class": "form-select"}),
            "customer_name": forms.TextInput(attrs={"class": "form-control"}),
            "product_name": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "distance": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "transport_required": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }