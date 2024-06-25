# music/spotify_utils.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.conf import settings
from .models import Song, UserInteraction

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='42f2cc13d26f4e1eb4319c80cf970c88',
    client_secret='0a41fba31ede44ea9cc40703f74418ef',
    redirect_uri="http://127.0.0.1:8000/api/callback/",
    scope="user-library-read user-top-read"
))

def get_user_top_tracks(user):
    top_tracks = sp.current_user_top_tracks(limit=50)
    for track in top_tracks['items']:
        save_interaction(user, track, 'top_track')

def save_track_to_db(track_info):
    song, created = Song.objects.get_or_create(
        spotify_id=track_info['id'],
        defaults={
            'name': track_info['name'],
            'artist': track_info['artists'][0]['name'],
            'genre': '',  # Spotify API does not directly provide genre for tracks
            'album': track_info['album']['name'],
            'release_date': track_info['album']['release_date'],
            'duration_ms': track_info['duration_ms'],
            'popularity': track_info['popularity'],
        }
    )
    return song

def save_interaction(user, track_info, interaction_type):
    song = save_track_to_db(track_info)
    UserInteraction.objects.create(user=user, song=song, interaction_type=interaction_type)
