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
    scope = 'user-read-private user-read-email'  # Adjust scopes based on your needs
    auth_url = f'https://accounts.spotify.com/authorize?client_id={settings.SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={settings.SPOTIFY_REDIRECT_URI}&scope={scope}'
    return redirect(auth_url)

def spotify_login(request):
    sp_oauth = SpotifyOAuth(
        client_id="42f2cc13d26f4e1eb4319c80cf970c88",
        client_secret="0a41fba31ede44ea9cc40703f74418ef",
        redirect_uri="http://127.0.0.1:8000/callback/",
        scope="user-library-read user-top-read"
    )

    auth_url = sp_oauth.get_authorize_url()
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
    access_token = request.session.get('spotify_access_token')

    if access_token:
        url = 'https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=5'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            top_tracks = response.json().get('items', [])  # Ensure to handle empty response
            logger.info(f"Fetched {len(top_tracks)} top tracks: {top_tracks}")  # Use logger for debugging
            context = {'top_tracks': top_tracks}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching top tracks: {str(e)}")  # Log error for debugging
            context = {'error_message': f'Error fetching top tracks: {str(e)}'}
    else:

        context = {'error_message': 'No Spotify access token available.'}

    return render(request, 'index.html', context)
