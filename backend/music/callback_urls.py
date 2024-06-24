# your_app/callback_urls.py

from django.urls import path
from . import views  # Import your views module

urlpatterns = [
    path('', views.spotify_callback, name='spotify_callback'),
]
