from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput, PasswordInput, EmailInput, Select
from .models import *


class BeerForm(forms.ModelForm):

    name = forms.CharField()
    description = forms.CharField()
    style = forms.CharField()
    class Meta:
        model = BEER
        fields = ['name', 'description', 'style']


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True,
                               widget=TextInput(
                                     attrs={'class': "form-control",
                                            'placeholder': "Username"}))
    password1 = forms.CharField(max_length=30, required=True,
                               widget=PasswordInput(
                                     attrs={'class': "form-control",
                                            'placeholder': "Enter Password"}))
    password2 = forms.CharField(max_length=30, required=True,
                                widget=PasswordInput(
                                     attrs={'class': "form-control",
                                            'placeholder': "Repeat Password"}))
    email = forms.EmailField(required=True,
                             widget=EmailInput(
                                attrs={'class': "form-control",
                                       'placeholder': "Email"}))
    first_name = forms.CharField(max_length=30, required=False,
                                 widget=TextInput(
                                     attrs={'class': "form-control",
                                            'placeholder': "First Name"}))
    last_name = forms.CharField(max_length=30, required=False,
                                widget=TextInput(
                                    attrs={'class': "form-control",
                                           'placeholder': "Last Name"}))
    city = forms.CharField(max_length=50, required=False,
                           widget=TextInput(
                               attrs={'class': "form-control",
                                      'placeholder': "City"}))
    state = forms.CharField(max_length=50, required=False,
                            widget=Select(attrs={'class': ("form-select")},
                                          choices=STATES))
    zip_code = forms.CharField(max_length=10, required=False,
                               widget=TextInput(
                                   attrs={'class': "form-control",
                                          'placeholder': "Zip Code"}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name',
                  'last_name', 'city', 'state', 'zip_code')


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100,
                            widget=forms.TextInput(attrs={'class':
                                                          'form-control'}))
