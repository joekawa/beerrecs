from django.shortcuts import render, get_object_or_404, redirect
from main.models import *
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, BeerForm, SearchForm, LoginForm
from django.contrib.admin.options import get_content_type_for_model
from django.urls import reverse
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q


def home(request):

    return render(request, 'home.html', {'message': 'Welcome to my home page',
                                         })


def contact_us(request):
    return render(request, 'contact_us.html')


def about_us(request):
    return render(request, 'about_us.html')


def search(request):
    form = SearchForm()
    results = []

    if request.GET.get('query'):
        query = request.GET.get('query')
        print(query)
        results2 = BREWERY.objects.filter(Q(name__icontains=query))
        results1 = BEER.objects.filter(Q(name__icontains=query) |
                                       Q(brewery__in=results2))
        results = list(results1) + list(results2)
    return render(request, 'search.html', {'results': results,
                                           'form': form})


def beer_list(request):
    beers = BEER.objects.all()
    return render(request, 'beer_list.html', {'beers': beers})


def my_beers(request):
    return render(request, 'my_beers.html', {'message': 'My Beers Success'})


def beer(request, id):
    beer = get_object_or_404(BEER, id=id)
    beer_upvotes = ACTIVITY.objects.filter(
      content_type=get_content_type_for_model(beer), activity='U',
      object_id=beer.pk).count()
    beer_downvotes = ACTIVITY.objects.filter(
      content_type=get_content_type_for_model(beer),
      activity='D', object_id=beer.pk).count()
    beer_favorites = ACTIVITY.objects.filter(
      content_type=get_content_type_for_model(beer), activity='F',
      object_id=beer.pk).count()
    beer_tags = TAG.objects.filter(beer=beer)

    return render(request, 'beer.html', {'beer': beer,
                                         'upvotes': beer_upvotes,
                                         'downvotes': beer_downvotes,
                                         'favorites': beer_favorites,
                                         'beer_tags': beer_tags
                                         })


def brewery(request, id):
    brewery = get_object_or_404(BREWERY, id=id)
    beers = BEER.objects.filter(brewery=brewery)

    return render(request, 'brewery.html', {'brewery': brewery,
                                            'beers': beers
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
        for f in form:
              print(f.name, f.errors)
        if form.is_valid():
            # authenticate the user and log them in
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            zip_code = form.cleaned_data.get('zip_code')
            state = form.cleaned_data.get('state')
            city = form.cleaned_data.get('city')
            user = User.objects.create_user(username=username,
                                            password=password)
            user.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            profile = PROFILE.objects.create(user=user,
                                             first_name=first_name,
                                             last_name=last_name,
                                             email=email,
                                             zip_code=zip_code,
                                             state=state,
                                             city=city)
            profile.save()
            print('created user')
            return redirect('main:home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)

    return redirect('main:home')


def beer_upvote(request, beer_id):
    beer = BEER.objects.get(id=beer_id)

    try:
        a = ACTIVITY.objects.exclude(activity='F').get(user=request.user,
                                      content_type=get_content_type_for_model(beer),
                                      object_id=beer.pk)
        if a.activity == 'D':
            a.activity = 'U'
            a.save()
        else:
            pass
    except ACTIVITY.DoesNotExist:
        ACTIVITY.objects.create(user=request.user, activity='U',
                                content_object=beer, object_id=beer.pk)
    beer.save()
    return redirect(reverse('main:beer', args=[beer_id]))


def beer_downvote(request, beer_id):
    beer = BEER.objects.get(id=beer_id)

    try:
        a = ACTIVITY.objects.exclude(activity='F').get(user=request.user,
                                 content_type=get_content_type_for_model(beer),
                                 object_id=beer.pk)
        if a.activity == 'U':
            a.activity = 'D'
            a.save()
        else:
            pass
    except ACTIVITY.DoesNotExist:
        ACTIVITY.objects.create(user=request.user, activity='D',
                                content_object=beer, object_id=beer.pk)
    beer.save()
    return redirect(reverse('main:beer', args=[beer_id]))


def beer_favorite(request, beer_id):
    beer = BEER.objects.get(id=beer_id)

    try:
        a = ACTIVITY.objects.get(user=request.user,
                                 content_type=get_content_type_for_model(beer),
                                 object_id=beer.pk,
                                 activity='F')

    except ACTIVITY.DoesNotExist:
        ACTIVITY.objects.create(user=request.user, activity='F',
                                content_object=beer, object_id=beer.pk)
    beer.save()
    return redirect(reverse('main:beer', args=[beer_id]))


def create_beer(request):
    if request.method == 'POST':
        form = BeerForm(request.POST)
        if form.is_valid():
            beer = form.save(commit=False)
            beer.created_by = request.user
            beer.save()
            return redirect(reverse('main:beer', args=[beer.id]))
    else:
        form = BeerForm()
    return render(request, 'create_beer.html', {'form': form})


def tag_beer(request, beer_id):
    if request.method == 'POST':
        beer_tag = request.POST.get('beer_tag')
        beer = BEER.objects.get(id=beer_id)
        TAG.objects.create(tag=beer_tag, beer=beer, created_by=request.user)
        print('tag on beer created')
    return redirect(reverse('main:beer', args=[beer_id]))


def tag_upvote(request, tag_id):
    if request.method == 'POST':
        tag = TAG.objects.get(id=tag_id)
        print(tag)
        try:
            a = ACTIVITY.objects.get(user=request.user,
                                      content_type=get_content_type_for_model(tag),
                                      object_id=tag.pk)
            print(a.activity)
            if a.activity == 'D':
                a.activity = 'U'
                a.save()
                print('changing flag')
            else:
                pass
        except ACTIVITY.DoesNotExist:
            ACTIVITY.objects.create(user=request.user, activity='U',
                                    content_object=tag, object_id=tag.pk)
            print('creating upvote')
    tag.save()
    return redirect(reverse('main:beer', args=[tag.beer.pk]))


def tag_downvote(request, tag_id):
    if request.method == 'POST':
        tag = TAG.objects.get(id=tag_id)
        try:
            a = ACTIVITY.objects.get(user=request.user,
                                      content_type=get_content_type_for_model(tag),
                                      object_id=tag.pk)
            if a.activity == 'U':
                a.activity = 'D'
                a.save()
            else:
                pass
        except ACTIVITY.DoesNotExist:
            ACTIVITY.objects.create(user=request.user, activity='D',
                                    content_object=tag, object_id=tag.pk)
    tag.save()
    return redirect(reverse('main:beer', args=[tag.beer.pk]))


