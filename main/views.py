from django.shortcuts import render, get_object_or_404
from main.models import *


def home(request):
    return render(request, 'home.html', {'message': 'Welcome to my home page'})


def search(request):
    return render(request, 'search.html', {'message': 'Search successful'})


def all_beers(request):
    return render(request, 'all_beers.html', {'message': 'All Beers success'})


def my_beers(request):
    return render(request, 'my_beers.html', {'message': 'My Beers Success'})


# ! PUT IN 2 AS A PLACEHOLDER ID
def beer(request, id):
    beer = get_object_or_404(BEER, id=id)

    return render(request, 'beer.html', {'name': beer.name,
                                         'description': beer.description,
                                         'brewery': 'Coors Light'
                                         })
