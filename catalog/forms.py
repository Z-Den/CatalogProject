from django import forms
from .models import Order, Product

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['discount']
        widgets = {
            'discount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'max': '100'
            })
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['brand', 'sugar_content', 'volume', 'is_alcoholic', 'flavor', 'expiration_date', 'category']
        widgets = {
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }


# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['brand', 'sugar_content', 'volume', 'is_alcoholic', 'flavor', 'expiration_date', 'category']
