from django import forms

class ClaimOrderForm(forms.Form):
    order_id = forms.IntegerField()
