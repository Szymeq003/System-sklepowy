from django import forms
from .models import Product, Order, OrderItem
from django.forms import inlineformset_factory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'stock']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'status']

OrderItemFormSet = inlineformset_factory(
    Order, 
    OrderItem, 
    fields=['product', 'quantity'], 
    extra=1, 
    can_delete=True
)
