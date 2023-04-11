from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class BeerForm(forms.ModelForm):

    name = forms.CharField()
    description = forms.CharField()
    style = forms.CharField()
    class Meta:
        model = BEER
        fields = ['name', 'description', 'style']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    city = forms.CharField(max_length=50, required=False)
    state = forms.CharField(max_length=50, required=False)
    zip_code = forms.CharField(max_length=10, required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name',
                  'last_name', 'city', 'state', 'zip_code')
