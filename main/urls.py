from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.search, name='search'),
    path('beer_list', views.beer_list, name='beer_list'),
    path('my_beers', views.my_beers, name='my_beers'),
    path('beer/<id>', views.beer, name='beer'),
    path('brewery/<id>', views.brewery, name='brewery'),
    path('favorites/<user_id>', views.favorites, name='favorites'),
    path('signup', views.signup, name='signup'),
    path('login', views.login_view, name='login'),
]
