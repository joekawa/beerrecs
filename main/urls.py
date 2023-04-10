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
    path('favorites/', views.favorites, name='favorites'),
    path('signup', views.signup, name='signup'),
    path('login', views.login_view, name='login'),
    path('beer_upvote/<beer_id>', views.beer_upvote, name='beer_upvote'),
    path('beer_downvote/<beer_id>', views.beer_downvote, name='beer_downvote'),
    path('beer_favorite/<beer_id>', views.beer_favorite, name='beer_favorite'),
]
