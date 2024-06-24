# your_app/callback_urls.py

from django.urls import path
from . import views  # Import your views module

urlpatterns = [
    path('login', views.authorize_spotify, name="login"),
    path('callback/', views.spotify_callback, name="callback"),
    path('index',  views.index, name='index'),
    path('recommended',  views.recommended, name='recommended'),
]
