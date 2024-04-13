from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    id = models.AutoField(primary_key=True)
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12)
    profile = models.ImageField(upload_to='stories/author/images/')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()
    pen_name = models.CharField(max_length=100)
    is_premium = models.BooleanField(default=False) 

    
    def __str__(self):
        return self.name
    


class AddPortfolio(models.Model):
    PORTFOLIO_CHOICES = [
        ('Medium', 'Medium'),
        ('Webite', 'Website'),
        ('Other', 'Other'), 
        ('social', 'Social Media'),
    ]
    id=models.AutoField(primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='portfolios')
    portfolio = models.CharField(max_length=100, choices=PORTFOLIO_CHOICES)
    link = models.CharField(max_length=100)


    def __str__(self):
        return self.portfolio+ ' - ' + self.author.name


