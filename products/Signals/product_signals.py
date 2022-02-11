from django.db.models.signals import pre_save
from products.models import Product
from django.dispatch import receiver
from django.utils.text import slugify
import random
import string

sr = random.SystemRandom()


@receiver(pre_save, sender=Product)
def slug_creator(sender, instance, *agrs, **kwargs):
	if instance.pk is None:
		try:
			instance.slug = slugify(f"{instance.title}")
		except:
			ch = sr.choices(string.digits, k=3)
			ch += sr.choices(string.ascii_letters, k=5)
			sr.shuffle(ch)
			ch = ''.join(ch)
			instance.slug = slugify(f"{instance.title}-{ch}")
