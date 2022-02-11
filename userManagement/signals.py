import profile
from django.db.models.signals import pre_save, post_save
from .models import UserAccount, Profile
from django.dispatch import receiver
from django.utils.text import slugify
import random
import string

sr = random.SystemRandom()


@receiver(post_save, sender=UserAccount)
def slug_creator(sender, instance,created, *agrs, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.slug = slugify(instance.username)
        instance.profile.save()