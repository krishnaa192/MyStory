
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm

class CandidateSignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2')


class AuthorForm(forms.ModelForm):
    class Meta:
        model=Author
        fields=['name','phone','bio','pen_name','profile']



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



class AddPortfolioForm(forms.ModelForm):
    class Meta:
        model=AddPortfolio
        fields=['portfolio','link']
