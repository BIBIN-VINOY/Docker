from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile


# Create Profile automatically when a User is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if created:
        Profile.objects.create(user=instance)


# Save Profile whenever the User is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):

    if hasattr(instance, 'profile'):
        instance.profile.save()


# Delete User automatically when a Profile is deleted
@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):

    if instance.user:
        instance.user.delete()