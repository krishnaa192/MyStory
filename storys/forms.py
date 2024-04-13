
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm



class StoryForm(forms.ModelForm):
    class Meta:
        model=Story
        fields=['title','description','image','category','audience','language','tag','premium_story']

class PartForm(forms.ModelForm):
    class Meta:
        model=Part
        fields=['part_image','name','text']


class CreatePlaylistForm(forms.ModelForm):
    class Meta:
        model=CreatePlaylist
        fields=['name','description']


