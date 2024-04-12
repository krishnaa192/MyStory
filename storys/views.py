from django.shortcuts import render, redirect, HttpResponse
from .models import *
from .decorator import *
from django.shortcuts import get_object_or_404
from .forms import *
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def header(request):
    user = request.user
    author = Author.objects.get(user=user)
    return render(request, 'header.html', {'author': author})
# Create your views here.

def Home(request): 
    cat = Category.objects.all()
    trending = Story.objects.all()[:6]
    first_trending = Story.objects.all()[:1]
    story = Story.objects.filter(category__in=cat)
    part = Part.objects.filter(story__in=story)
    
    context = {'story': story, 'part': part, 'cat': cat,
               'trending': trending, 'first_trending': first_trending}
    
    if request.user.is_authenticated:
        user = request.user
        author = Author.objects.get(user=user)
        if author:
            context['user'] = user
            context['author'] = author

    return render(request, 'home.html', context)

def read_parts(request, story_id, part_id):
    user = request.user
    author = get_object_or_404(Author, user=user)
    part = get_object_or_404(Part, id=part_id, story_id=story_id)
    return render(request, 'parts.html', {'part': part, 'author': author})


def read_story(request, id):
    user = request.user
    author = Author.objects.get(user=user)
    story = Story.objects.get(id=id)
    part = Part.objects.filter(story=story)
    return render(request, 'story.html', {'story': story, 'author': author, 'part': part})

def search(request):
    query = request.GET.get('query')  
    if query:
        search_terms = query.split()  # Split the query into individual terms
        queryset = Story.objects.all()
        authors = Author.objects.all()
        parts = Part.objects.filter(story__in=queryset)
        for term in search_terms:
            queryset = queryset.filter(
                Q(title__icontains=term) | Q(category__name__icontains=term) | Q(language__icontains=term)
            )
            authors = authors.filter(name__icontains=term)
            parts = parts.filter(
                Q(name__icontains=term)
            )
        story = Story.objects.filter(title__icontains=query)
        return render(request, 'search.html', {'results': queryset, 'query': query, 'authors': authors, 'parts': parts, 'story': story})
    else:
        # Handle the case where 'query' key is not present in request.GET
        return render(request, 'search.html', {'story': None, 'query': None})




def paid_content(request):
    return render(request, paid_content.html)


def paid_story(request):
    user = request.user
    author = Author.objects.get(user=user)
    context = {'author': author}
    return render(request, 'paid.html', context)


def add_story(request):
    user = request.user
    try:
        author = Author.objects.get(user=user)
    except Author.DoesNotExist:
        return HttpResponse("You need to create an author profile first.")

    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = author
            story.save()
            return redirect('user_story', id=story.id)
    else:
        form = StoryForm()
    return render(request, 'storyform.html', {'form': form, 'author': author})


def edit_story(request, id):
    user = request.user
    author = Author.objects.get(user=user)
    story = Story.objects.get(id=id)
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES, instance=story)
        if form.is_valid():
            form.save()
            return redirect('user_story')
    else:
        form = StoryForm(instance=story)
    return render(request, 'storyform.html', {'form': form, 'author': author})


def delete_story(request, id):
    story = Story.objects.get(id=id)
    story.delete()
    return redirect('user_story')


def delete_part(request, story_id, part_id):
    part = Part.objects.get(id=part_id)
    part.delete()
    return redirect('story', id=story_id)


def user_story(request):
    user = request.user
    author = Author.objects.get(user=user)
    stories = Story.objects.filter(author=author)
    paginator = Paginator(stories, 5)  # Show 6 stories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'added_story.html', {'stories': stories, 'author': author, 'page_obj': page_obj})

@is_premium_required
def premium_story(request):
    user = request.user
    author = Author.objects.get(user=user)
    stories = Story.objects.filter(author=author, premium_story=True)
    paginator = Paginator(stories, 5)  # Show 6 stories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'premiumstory.html', {'stories': stories, 'author': author, 'page_obj': page_obj})

def author_story(request):
    user = request.user
    author = Author.objects.get(user=user)
    story = Story.objects.filter(author=author)
    return render(request, 'author_story.html', {'story': story, 'author': author})


def add_part(request, id):
    user = request.user
    author = Author.objects.get(user=user)
    story = Story.objects.get(id=id)
    if request.method == 'POST':
        # Pass the story object to the form
        form = PartForm(request.POST, request.FILES, initial={'story': story})
        if form.is_valid():
            # Get the latest part number for the story
            latest_part_number = Part.objects.filter(
                story=story).order_by('-part_number').first()
            if latest_part_number:
                next_part_number = latest_part_number.part_number + 1
            else:
                next_part_number = 1

            part = form.save(commit=False)
            part.story = story
            part.part_number = next_part_number  # Assign the auto-incremented part number
            part.save()
            return redirect('story', id=story.id)
    else:
        # Pass the story object to the form
        form = PartForm(initial={'story': story})
    return render(request, 'partform.html', {'form': form, 'story': story, 'author': author})


def create_playlist(request):
    user = request.user
    author = Author.objects.get(user=user)
    if request.method == 'POST':
        form = CreatePlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.author = author
            playlist.save()
            return redirect('home')
    else:
        form = CreatePlaylistForm()
    return render(request, 'create_playlist.html', {'form': form, 'author': author})
# user


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


def author_Profile(request):
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


def Profile(request, name):
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


# # payemtn

def checkout(request):
    return render(request, 'checkout.html')