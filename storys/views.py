from django.shortcuts import render, redirect, HttpResponse
from .models import *
from .decorator import *
from account.models import *
from django.shortcuts import get_object_or_404
from .forms import *
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import F, ExpressionWrapper, fields
from django.utils import timezone

from django.db.models import Count


def header(request):
    user = request.user
    author = Author.objects.get(user=user)
    return render(request, 'header.html', {'author': author})


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

def explore(request):
    cat = Category.objects.all()
    stories = Story.objects.all()
    part = Part.objects.filter(story__in=stories)
    recent = Story.objects.all().order_by('-date')[:3]
    paginator = Paginator(stories, 8)  # Show 6 stories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    #make time difffernce of post  in hours
    context = {'stories': stories, 'part': part, 'cat': cat, 'recent': recent, 'page_obj': page_obj, 'paginator': paginator}
    return render(request, 'explore.html', context)


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
    

##parts handling

def read_parts(request, story_id, part_id):
    if not  request.user.is_authenticated:
        return redirect('login')
    user = request.user
    author = get_object_or_404(Author, user=user)
    part = get_object_or_404(Part, id=part_id, story_id=story_id)
    return render(request, 'parts.html', {'part': part, 'author': author})

@login_required
def add_part(request, id):
    if not  request.user.is_authenticated:
        return redirect('login')
 
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

@login_required
def edit_part(request, story_id, part_id):
    user = request.user
    try:
        author = Author.objects.get(user=user)
        story = Story.objects.get(id=story_id)
        part = Part.objects.get(id=part_id)

        if author != story.author:
            return HttpResponse("You are not authorized to edit this part.")

        if request.method == 'POST':
            form = PartForm(request.POST, request.FILES, instance=part, initial={'story': story})
            if form.is_valid():
                form.save()
                return redirect('story', id=story_id)
        else:
            form = PartForm(instance=part)

        return render(request, 'editpart.html', {'form': form, 'story': story, 'author': author, 'part': part})

    except (Author.DoesNotExist, Story.DoesNotExist, Part.DoesNotExist):
        return HttpResponse("Invalid request or resource does not exist.")


@login_required
def delete_part(request, story_id, part_id):
    if not  request.user.is_authenticated:
        return redirect('login')
    user=request.user
    author=Author.objects.get(user=user)
    story = Story.objects.get(id=id)
    if story.author != author:
        return HttpResponse("You are not authorized to delete this story.")
    else:
        part = Part.objects.get(id=part_id)
        part.delete()
    return redirect('story', id=story_id)



# story handling

def read_story(request, id):
    story = Story.objects.get(id=id)
    part = Part.objects.filter(story=story)
    story_author=story.author
    if request.user.is_authenticated:
        user = request.user
        author = Author.objects.get(user=user)

    return render(request, 'story.html', {'story': story, 'author': author, 'part': part, 'story_author':story_author})


@login_required
def add_story(request):
    if not  request.user.is_authenticated:
        return redirect('login')
    try:
        user = request.user
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

@login_required
def edit_story(request, id):
    if not  request.user.is_authenticated:
        return redirect('login')
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

@login_required
def delete_story(request, id):
    if not  request.user.is_authenticated:
        return redirect('login')
    user=request.user
    author=Author.objects.get(user=user)
    story = Story.objects.get(id=id)
    if story.author != author:
        return HttpResponse("You are not authorized to delete this story.")
    story.delete()
    return redirect('user_story')

@login_required
def user_story(request):
    user = request.user
    author = Author.objects.get(user=user)
    stories = Story.objects.filter(author=author)
    paginator = Paginator(stories, 5)  # Show 6 stories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'added_story.html', {'stories': stories, 'author': author, 'page_obj': page_obj})




##premium content handling

def paid_content(request):
    if not  request.user.is_authenticated:
        return redirect('login')
    author=Author.objects.get(user=request.user)
    if not request.author.is_premium:
        return redirect('checkout')
    return render(request, paid_content.html)


def paid_story(request):
    if not  request.user.is_authenticated:
        return redirect('login')
    user = request.user
    author = Author.objects.get(user=user)
    context = {'author': author}
    return render(request, 'paid.html', context)

@is_premium_required
def premium_story(request):
    if not  request.user.is_authenticated:
        return redirect('login')

    user = request.user
    author = Author.objects.get(user=user)
    stories = Story.objects.filter(author=author, premium_story=True)
    cat= Category.objects.filter(story__in=stories)
    paginator = Paginator(stories, 5)  # Show 6 stories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'premiumstory.html', {'stories': stories, 'author': author, 'page_obj': page_obj, 'cat': cat})


##category handling
def categoryPage(request, name):
    cat = Category.objects.get(name=name)
    story = Story.objects.filter(category=cat)
    part = Part.objects.filter(story__in=story)
    other_categories = Category.objects.exclude(name=name)
    recent = Story.objects.filter(category=cat).order_by('-date')[:3]
    paginator = Paginator(story, 8)  # Show 6 stories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'story': story, 'part': part, 'cat': cat, 'other_categories': other_categories, 'recent': recent, 'page_obj': page_obj, 'paginator': paginator}

    return render(request, 'category.html', context)



# comment and likes handling

def likes(request):
    if not  request.user.is_authenticated:
        return redirect('login')
    user = request.user
    author = Author.objects.get(user=user)
    if request.method == 'POST':
        story_id = request.POST.get('story_id')
        story = Story.objects.get(id=story_id)
        like = Likes.objects.create(liked_user=author)
        like.post.add(story)
        like.save()
    return redirect('/')
     
    





## library handling
@login_required
def create_playlist(request):
    if not  request.user.is_authenticated:
        return redirect('login')
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


# # payemt hand;ing
@login_required
def checkout(request):
    return render(request, 'checkout.html')