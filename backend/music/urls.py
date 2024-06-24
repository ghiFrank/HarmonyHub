from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SongViewSet, UserInteractionViewSet, RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import fetch_spotify_data,authorize_spotify,index

router = DefaultRouter()
router.register(r'songs', SongViewSet)
router.register(r'interactions', UserInteractionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('fetch-spotify-data/', fetch_spotify_data, name='fetch_spotify_data'),
    path('accounts/', include('allauth.urls')),
    path('login', authorize_spotify, name="login"),
    path('index', index, name='index'),
]
