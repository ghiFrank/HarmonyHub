
from django.shortcuts import render, redirect
from spotipy.oauth2 import SpotifyOAuth
import requests
from requests.auth import HTTPBasicAuth
import base64
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse


def authorize_spotify(request):
    scope = 'user-read-private user-read-email user-library-read user-top-read'
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
        base64_bytes = base64.b64encode(f'{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}'.encode("ascii"))
        base64_string = base64_bytes.decode("ascii")
        data = {
            'code': code,
            'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
            'grant_type': 'authorization_code'
        }
        token_info = requests.post('https://accounts.spotify.com/api/token',data=data,headers={'Content-Type': 'application/x-www-form-urlencoded'},auth=HTTPBasicAuth(settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_CLIENT_SECRET))
        # Store access token securely (e.g., in session)
        if 'access_token' in token_info.json():
            return redirect(f'{settings.FRONTEND_URL}?access_token={token_info.json()['access_token']}')
        else:
            return redirect(f'{settings.FRONTEND_URL}/login?error=Failed to retrieve access token')
    else:
        return redirect(f'{settings.FRONTEND_URL}/login?error=Authorization code not found')


def index(request):
    print(request.session.keys())
    if 'spotify_access_token' in request.session:
        access_token = request.session['spotify_access_token']
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
                'spotify_url': track['external_urls']['spotify']
            })
        
        response = {
            'top_tracks': top_tracks_with_images,
            'code': 0 
        }
    else:
        response = {'error_message': 'No Spotify access token available.',
                    'code': 1 }

    return JsonResponse(response)


# Function to fetch user's top tracks
def get_top_tracks(access_token):
    url = 'https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=5'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    print(response.text)
    response.raise_for_status()  # Raise error for non-200 status codes
    return response.json()['items']

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
                'spotify_url': track['external_urls']['spotify']
            })
        
        context = {
            'recommended_tracks': recommended_tracks_with_images,
        }
    else:
        context = {'error_message': 'No Spotify access token available.'}
    
    return render(request, 'recommended.html', context)

