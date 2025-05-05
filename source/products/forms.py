from django import forms
from . import models

class DesignForm(forms.ModelForm):
    class Meta:
        model = models.Design
        fields = ['name', 'image']
