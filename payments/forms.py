from django import forms

class PaymentForm(forms.Form):
    name = forms.CharField(max_length=255, label='상품명')
    amount = forms.IntegerField(min_value=0, label='금액')
