from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import authorize_spotify,spotify_callback,index,recommended

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/', include('allauth.urls')),
    path('login', authorize_spotify, name="login"),
    path('callback/', spotify_callback, name="callback"),
    path('index',  index, name='index'),
    path('recommended',  recommended, name='recommended'),
]
