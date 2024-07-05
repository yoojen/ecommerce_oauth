from django import forms
from .models import Product, BillingAddress


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
