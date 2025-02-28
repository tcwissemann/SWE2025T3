from django import forms

class cartForm(forms.Form):
    cart = forms.JSONField(widget=forms.widgets.HiddenInput)