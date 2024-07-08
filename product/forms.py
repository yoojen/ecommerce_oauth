from typing import Any
from django import forms
from .models import Order, Product, BillingAddress


class UploadForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name",
                  "type",
                  "category",
                  "price",
                  "image"]

class CheckOutForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = "__all__"

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["payment_method", "amount_payed"]
    
        
