from rest_framework import viewsets
from .models import Song, UserInteraction
from .serializers import SongSerializer, UserInteractionSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .spotify_utils import get_user_top_tracks
from django.http import HttpResponse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from django.shortcuts import render
from django.conf import settings
import logging


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsAuthenticated]

class UserInteractionViewSet(viewsets.ModelViewSet):
    queryset = UserInteraction.objects.all()
    serializer_class = UserInteractionSerializer
    permission_classes = [IsAuthenticated]

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_active = True  # Ensure user is active
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

def authorize_spotify(request):
    # Redirect user to Spotify authorization URL
    scope = 'user-read-private user-read-email user-library-read user-top-read'  # Adjust scopes based on your needs
    auth_url = f'https://accounts.spotify.com/authorize?client_id={settings.SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={settings.SPOTIFY_REDIRECT_URI}&scope={scope}'
    return redirect(auth_url)


def spotify_callback(request):
    # Handle callback from Spotify after user authorization
    code = request.GET.get('code')
    error = request.GET.get('error')

    if error:
        # Handle error from Spotify authorization
        return render(request, 'error.html', {'error_message': error})

    if code:
        # Exchange authorization code for access token
        token_url = 'https://accounts.spotify.com/api/token'
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
            'client_id': settings.SPOTIFY_CLIENT_ID,
            'client_secret': settings.SPOTIFY_CLIENT_SECRET,
        }

        # Make POST request to Spotify token endpoint
        response = requests.post(token_url, data=payload)
        response_data = response.json()
        # Store access token securely (e.g., in session)
        if 'access_token' in response_data:
            request.session['spotify_access_token'] = response_data['access_token']
            return redirect('/api/index')  # Redirect to homepage or desired page
        else:
            return render(request, 'error.html', {'error_message': 'Failed to retrieve access token'})
    else:
        return render(request, 'error.html', {'error_message': 'Authorization code not found'})

def fetch_spotify_data(request):
    user = request.user
    get_user_top_tracks(user)
    return redirect('/profile')  # Redirect to a profile or dashboard page


logger = logging.getLogger(__name__)



def index(request):
    # Fetch user's Spotify access token
    access_token = request.session['spotify_access_token']
    if access_token:
        # Function to fetch user's top tracks
        def get_top_tracks(access_token):
            url = 'https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=5'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise error for non-200 status codes
            return response.json()['items']
        
        # Fetch user's top tracks with cover images
        top_tracks = get_top_tracks(access_token)
        top_tracks_with_images = []
        for track in top_tracks:
            # Fetch cover image URL (first image in 'images' array)
            cover_image_url = track['album']['images'][0]['url'] if track['album']['images'] else None
            top_tracks_with_images.append({
                'name': track['name'],
                'artists': track['artists'],
                'cover_image_url': cover_image_url,
            })
        
        context = {
            'top_tracks': top_tracks_with_images,
        }
    else:
        context = {'error_message': 'No Spotify access token available.'}
    
    return render(request, 'index.html', context)

def recommended(request):
    # Fetch user's Spotify access token
    access_token = request.session['spotify_access_token']
    
    if access_token:
        # Function to fetch recommended tracks based on user's top tracks
        def get_recommendations(access_token, top_tracks_ids):
            url = 'https://api.spotify.com/v1/recommendations'
            seed_tracks = ','.join(top_tracks_ids)
            params = {
                'limit': 5,
                'seed_tracks': seed_tracks,
            }
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
            }
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # Raise error for non-200 status codes
            return response.json()['tracks']
        
        # Function to fetch user's top tracks
        def get_top_tracks(access_token):
            url = 'https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=5'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise error for non-200 status codes
            return response.json()['items']

        # Fetch user's top tracks IDs
        top_tracks = get_top_tracks(access_token)
        top_tracks_ids = [track['id'] for track in top_tracks]
        
        # Fetch recommended tracks with cover images based on top tracks
        recommended_tracks = get_recommendations(access_token, top_tracks_ids)
        recommended_tracks_with_images = []
        for track in recommended_tracks:
            # Fetch cover image URL (first image in 'images' array)
            cover_image_url = track['album']['images'][0]['url'] if track['album']['images'] else None
            recommended_tracks_with_images.append({
                'name': track['name'],
                'artists': track['artists'],
                'cover_image_url': cover_image_url,
            })
        
        context = {
            'recommended_tracks': recommended_tracks_with_images,
        }
    else:
        context = {'error_message': 'No Spotify access token available.'}
    
    return render(request, 'recommended.html', context)

