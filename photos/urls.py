from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', Albums.as_view(), name='home'),
    path('add_album/', AddAlbum.as_view(), name='add_album'),
    path('add_photo/', AddPhoto.as_view(), name='add_photo'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('album/<int:album_id>/', PhotoView.as_view(), name='album')
]
