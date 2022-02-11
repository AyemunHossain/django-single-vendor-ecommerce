from django.db import IntegrityError, transaction
from django.db.models.signals import post_save
from products.models import Category
from django.dispatch import receiver
from django.utils.text import slugify
import random
import string

sr = random.SystemRandom()

@receiver(post_save, sender=Category)
def slug_creator(sender, instance, *agrs, **kwargs):
    	
		# try:	
		# 	with transaction.atomic():
		# 		instance.slug = slugify(f"{instance.title}")
		# 		instance.save()
		# except :
		# 	ch = sr.choices(string.digits, k=3)
		# 	ch += sr.choices(string.ascii_letters, k=5)
		# 	sr.shuffle(ch)
		# 	ch = ''.join(ch)
		# 	instance.slug = slugify(f"{instance.title}-{ch}")
		# 	instance.save()
	pass