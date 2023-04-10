from django.shortcuts import render, get_object_or_404, redirect
from main.models import *
from django.contrib.auth import authenticate, login
from .forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.admin.options import get_content_type_for_model
from django.urls import reverse


def home(request):
    return render(request, 'home.html', {'message': 'Welcome to my home page'})


def search(request):
    return render(request, 'search.html', {'message': 'Search successful'})


def beer_list(request):
    beers = BEER.objects.all()
    return render(request, 'beer_list.html', {'beers': beers})


def my_beers(request):
    return render(request, 'my_beers.html', {'message': 'My Beers Success'})


def beer(request, id):
    beer = get_object_or_404(BEER, id=id)

    return render(request, 'beer.html', {'beer': beer
                                         })


def brewery(request, id):
    brewery = get_object_or_404(BREWERY, id=id)

    return render(request, 'brewery.html', {'name': brewery.name,
                                            'description': brewery.description,
                                            })


def favorites(request):
    # Get the current user
    user = request.user

    # Query the BEER model for all BEER objects with the user's favorite activity
    favorite_beers = BEER.objects.filter(activity__activity='F',
                                         activity__user=user)

    # Pass the favorite beers queryset to the template
    context = {'favorite_beers': favorite_beers}
    return render(request, 'favorites.html', context)


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


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def beer_upvote(request, beer_id):
    beer = BEER.objects.get(id=beer_id)

    a = ACTIVITY.objects.get(user=request.user,
                                       content_type=get_content_type_for_model(beer),
                                       object_id=beer.pk)
    if not a:
        ACTIVITY.objects.create(user=request.user, activity='U',
                                content_object=beer, object_id=beer.pk)
    elif a.activity == 'D':
        a.activity = 'U'
        a.save()

    elif a.activity == 'U':
        pass

    return redirect(reverse('main:beer', args=[beer_id]))


def beer_downvote(request, beer_id):
    beer = BEER.objects.get(id=beer_id)

    a = ACTIVITY.objects.get(user=request.user,
                                       content_type=get_content_type_for_model(beer),
                                       object_id=beer.pk)
    if not a:
        ACTIVITY.objects.create(user=request.user, activity='D',
                                content_object=beer, object_id=beer.pk)
    elif a.activity == 'U':
        a.activity = 'D'
        a.save()

    elif a.activity == 'D':
        pass

    return redirect(reverse('main:beer', args=[beer_id]))


def beer_favorite(request, beer_id):
    beer = BEER.objects.get(id=beer_id)

    a = ACTIVITY.objects.get(user=request.user,
                                       content_type=get_content_type_for_model(beer),
                                       object_id=beer.pk,
                                       activity= 'F')
    if not a:
        ACTIVITY.objects.create(user=request.user, activity='F',
                                content_object=beer, object_id=beer.pk)

    return redirect(reverse('main:beer', args=[beer_id]))
