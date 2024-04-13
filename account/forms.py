from storys.models import *
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


class AddPortfolioForm(forms.ModelForm):
    class Meta:
        model=AddPortfolio
        fields=['portfolio','link']
