from django.shortcuts import render


def home(request):
    return render(request, 'home.html', {'message': 'Welcome to my home page'})


def search(request):
    return render(request, 'search.html', {'message': 'Search successful'})


def all_beers(request):
    return render(request, 'all_beers.html', {'message': 'All Beers success'})


def my_beers(request):
    return render(request, 'my_beers.html', {'message': 'My Beers Success'})