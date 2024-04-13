from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from storys.decorator import *
from django.shortcuts import get_object_or_404
from .forms import *
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import F, ExpressionWrapper, fields
from django.utils import timezone

from django.db.models import Count


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CandidateSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('create-profile')
    else:
        form = CandidateSignupForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def author_Profile(request):
    if not  request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_premium:
        return redirect('checkout')
    user = request.user
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.email = user.email
            # Associate the profile with the user
            profile.save()
            return redirect('home')
    else:
        form = AuthorForm()
    return render(request, 'author_signup.html', {'form': form})

@login_required
def Profile(request, name):
    if not  request.user.is_authenticated:
        return redirect('login')
   
    user = request.user
    user = User.objects.get(username=name)
    story = Story.objects.filter(author__user=user)
    playlists = CreatePlaylist.objects.filter(author__user=user)
    play_count = playlists.count()
    playlist=playlists.order_by('-updated_at')[:6]
    story_count = story.count()
    author = Author.objects.get(user=user)
    name = author.name
    first_name = name.split()[0]
    last_name = name.split()[1]
    portfolio=AddPortfolio.objects.filter(author__user=user)
    params = {
        'author': author, 'story': story, 'story_count': story_count,
          'first_name': first_name, 'last_name': last_name, 'play_count':play_count, 'playlist': playlist, 'portfolio':portfolio}
    return render(request, 'user-profile.html', params)


@login_required
def edit_profile(request):
    user = request.user
    author = Author.objects.get(user=user)
    form = AuthorForm(instance=author)
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            form.save()
            return redirect('profile', name=user.username)
        else:
            form = AuthorForm(instance=author)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def add_portfolio(request):
    user=request.user
    form=AddPortfolioForm()
    if request.method=='POST':
        form=AddPortfolioForm(request.POST)
        if form.is_valid():
            portfolio=form.save(commit=False)
            portfolio.author=Author.objects.get(user=user)
            portfolio.save()
            return redirect('profile',name=user.username)
        else:
            form=AddPortfolioForm()
    return render(request,'add_portfolio.html',{'form':form})

def AuthorProfile(request,name):
    user=User.objects.get(username=name)
    story = Story.objects.filter(author__user=user)
    story_count = story.count()
    author = Author.objects.get(user=user)
    name = author.name
    first_name = name.split()[0]
    last_name = name.split()[1]
    portfolio=AddPortfolio.objects.filter(author__user=user)
    params = {
        'author': author, 'story': story, 'story_count': story_count,
          'first_name': first_name, 'last_name': last_name,  'portfolio':portfolio}
    return render(request, 'authors.html', params)

