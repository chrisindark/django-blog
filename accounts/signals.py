from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User, UserProfile


@receiver(post_save, sender=User)
def create_profile_on_user_save(sender, **kwargs):
    if kwargs.get('created', False):
        UserProfile.objects.get_or_create(user=kwargs.get('instance'))
