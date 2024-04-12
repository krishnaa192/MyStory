

from django.urls import path
from . import views

urlpatterns = [
    path('header/', views.header, name='header'),
    path('', views.Home, name='home'),
    path('read/<int:story_id>/<int:part_id>/', views.read_parts, name='read'),
    path('story/<int:id>/', views.read_story, name='story'),
    path('search/', views.search, name='search'),
   
    path('paid/', views.paid_story, name='paid'),
    path('premium-content/',views.paid_content,name="premium-content"),
    path('premium/',views.premium_story,name="premium"),
    path('add-story/',views.add_story,name="add-story"),
    path('edit-story/<int:id>/',views.edit_story,name="edit-story"),
    path('delete-story/<int:id>/',views.delete_story,name="delete-story"),
    path('remove-part/<int:story_id>/<int:part_id>/',views.delete_part,name="remove-part"),
    path('create-playlists/',views.create_playlist,name="create-playlists"),
    path('add-part/<int:id>/', views.add_part, name="add-part"),
    path('user-story/', views.user_story, name="user_story"),
    path('your-story/', views.author_story, name="author_story"),

#user

    path('login/', views.loginUser, name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/', views.registerUser, name='register'),
    path('profile/<str:name>/', views.Profile, name='profile'),
    path('create-profile/', views.author_Profile, name='create-profile'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('portfolio/', views.add_portfolio, name='add-portfolio'),


    path('checkout/', views.checkout, name='checkout'),
   
]
