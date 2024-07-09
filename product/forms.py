from typing import Any
from django import forms
from .models import Order, Product


class UploadForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name",
                  "type",
                  "category",
                  "price",
                  "image"]


PAYMENT_CHOICES = (
    ("MTN Rwanda", "MTN Mobile Money"),
    ("Airtel Rwanda", "Airtel Money ")
)
class CheckOutForm(forms.Form):
    province = forms.CharField(max_length=256)
    district = forms.CharField(max_length=256)
    sector=forms.CharField(max_length=256)
    amount_payed=forms.CharField(max_length=256)
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES)
