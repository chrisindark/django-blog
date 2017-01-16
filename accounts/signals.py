from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User

@receiver(post_save, sender=User)
def check_user_save(sender, **kwargs):
    print("sender", sender)
    print("kwargs", kwargs)
    # if kwargs.get('created', False):
    #     UserProfile.objects.get_or_create(user=kwargs.get('instance'))
