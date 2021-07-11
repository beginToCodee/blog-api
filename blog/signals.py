from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *


@receiver(post_save,sender=User)
def create_profile_signal(sender,**kwargs):
    instance = kwargs.get('instance')
    created = kwargs.get('created')
    if created:
        profile = Profile(user=instance)
        profile.save()
