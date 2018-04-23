from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Post


@receiver(post_save, sender=Post)
def check_post_save(sender, **kwargs):
    print("kwargs", kwargs)


