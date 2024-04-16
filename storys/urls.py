

from django.urls import path
from . import views

urlpatterns = [
    path('header/', views.header, name='header'),
    path('', views.Home, name='home'),
    path('read/<int:story_id>/<int:part_id>/', views.read_parts, name='read'),
    path('story/<int:id>/', views.read_story, name='story'),
    path('search/', views.search, name='search'),
    path('explore/', views.explore, name='explore'),
    path('category/<str:name>/', views.categoryPage, name='category'),
    path('add-story/',views.add_story,name="add-story"),
    path('edit-story/<int:id>/',views.edit_story,name="edit-story"),
    path('delete-story/<int:id>/',views.delete_story,name="delete-story"),
    path('remove-part/<int:story_id>/<int:part_id>/',views.delete_part,name="remove-part"),
    path('edit-part/<int:story_id>/<int:part_id>/', views.edit_part, name="edit-part"),
    path('create-playlists/',views.create_playlist,name="create-playlists"),
    path('add-part/<int:id>/', views.add_part, name="add-part"),
    path('user-story/', views.user_story, name="user_story"),
    path('like/', views.likes, name="like"),


#user
  #premium content and payment
    path('checkout/', views.checkout, name='checkout'),
     path('paid/', views.paid_story, name='paid'),
    path('premium-content/',views.paid_content,name="premium-content"),
    path('premium/',views.premium_story,name="premium"),
   
]
