from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal to create a Profile when a new User is created.
    """
    if created:
        Profile.objects.create(client=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Signal to save the Profile when the User instance is saved.
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()