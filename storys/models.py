from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from account.models import *




# model for category
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
AUDIENCE_CHOICES = [
        ('Everyone', 'Everyone'),
        ('Teen', 'Teens'),
        ('Adults', 'Adults'),
        ('Children', 'Children'),
    ]
LANGUAGE_CHOICES = [
        ('English', 'English'),
        ('Hindi', 'Hindi'),
        ('Marathi', 'Marathi'),
        ('Telugu', 'Telugu'),
        ('Tamil', 'Tamil'),
        ('Kannada', 'Kannada'),
        ('Bengali', 'Bengali'),
        ('Gujarati', 'Gujarati'),
        ('Odia', 'Odia'),
        ('Punjabi', 'Punjabi'),
        ('Malayalam', 'Malayalam'),
    ]
    # model for story
class Story(models.Model):
   

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    premium_story = models.BooleanField(default=False)
    description = models.TextField()  # Use lowercase for field name
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    audience = models.CharField(max_length=10, choices=AUDIENCE_CHOICES)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    date = models.DateField(auto_now_add=True)  # Automatically set the date
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='stories/story/images/')
    tag = models.CharField(max_length=100)
    date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# model for part
class Part(models.Model):
    #set id as autoincrement field
    id = models.AutoField(primary_key=True,unique=True,auto_created=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='parts')
    part_image = models.ImageField(upload_to='stories/part/images/')
    part_number = models.IntegerField()
    name = models.CharField(max_length=100,default='Untitled')
    text = RichTextField()

    def __str__(self):
        return self.story.title + ' - ' + str(self.part_number)
    

class CreatePlaylist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    author= models.ForeignKey(Author, on_delete=models.CASCADE, related_name='playlists')
    date = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    story = models.ManyToManyField(Story)
    
    def __str__(self):
        return self.name
    