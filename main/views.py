from django.shortcuts import render, get_object_or_404, redirect
from main.models import *
from django.contrib.auth import authenticate, login
from .forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm


def home(request):
    return render(request, 'home.html', {'message': 'Welcome to my home page'})


def search(request):
    return render(request, 'search.html', {'message': 'Search successful'})


def all_beers(request):
    return render(request, 'all_beers.html', {'message': 'All Beers success'})


def my_beers(request):
    return render(request, 'my_beers.html', {'message': 'My Beers Success'})


def beer(request, id):
    beer = get_object_or_404(BEER, id=id)

    return render(request, 'beer.html', {'name': beer.name,
                                         'description': beer.description,
                                         'brewery': 'Coors Light'  #!placeholder
                                         })


def brewery(request, id):
    brewery = get_object_or_404(BREWERY, id=id)

    return render(request, 'brewery.html', {'name': brewery.name,
                                            'description': brewery.description,
                                            })


def favorites(request, user_id):
    return render(request, 'favorites.html', {'favorite':  'This is my fave'})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # authenticate the user and log them in
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('main:home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
