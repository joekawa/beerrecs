from django import forms
from .models import *


class BeerInputForm(forms.ModelForm):
    class Meta:
        model = BEER
        fields = ('name', 'description', 'brewery')