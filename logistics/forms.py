from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_description', 'product_price', 'product_inventory', 'product_img', 'product_sale']