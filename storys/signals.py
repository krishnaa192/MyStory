from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Author

@receiver(post_save, sender=User)
def update_author_premium_status(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)
    instance.author.is_premium = instance.is_premium  # Assuming user's premium status is stored in is_premium
    instance.author.save()
