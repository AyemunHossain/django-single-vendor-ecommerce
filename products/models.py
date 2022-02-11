#Library imports
from ast import arg
from django.db import models
from simple_history.models import HistoricalRecords
from ckeditor.fields import RichTextField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.db import IntegrityError, transaction
import random
import string
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from .choices import CATEGORY_STATUS, PRODUCT_STATUS_CHOICES, PRODUCT_VISIBILITY_CHOICES


User = get_user_model()
sr = random.SystemRandom()

class Category(MPTTModel):

	parent 			= TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
	title 			= models.CharField(max_length=50)
	keywords 		= models.CharField(max_length=255)
	description 	= models.TextField(max_length=255)
	image 			= models.ImageField(blank=True, upload_to='images/')
	status 			= models.CharField(max_length=10, choices=CATEGORY_STATUS)
	slug 			= models.SlugField(blank=True,unique=True)
	create_at 		= models.DateTimeField(auto_now_add=True)
	update_at 		= models.DateTimeField(auto_now=True)


	def save(self, *args, **kwargs):
    
		#Saving the slug: if already exists then add random string with it
		if self.pk is None:
			self.slug = slugify(self.title)
			try:
				with transaction.atomic():
					super(Category, self).save(*args, **kwargs)
			except:
				ch = sr.choices(string.digits, k=1)
				ch += sr.choices(string.ascii_letters, k=2)
				sr.shuffle(ch)
				ch = ''.join(ch)
				self.slug = slugify(f"{self.title}-{ch}")
				try:
					super(Category, self).save(*args, **kwargs)
				except:
					self.save(*args, **kwargs)
    
	class MPTTMeta:
		order_insertion_by = ['title']
	    
	class Meta:
		verbose_name_plural = 'Categories'
	  
	def __str__(self):
		full_path = [self.title]
		k = self.parent
		while k is not None:
			full_path.append(k.title)
			k = k.parent
		return ' / '.join(full_path[::-1])


class Product(models.Model):
	title           = models.CharField(max_length=450, default='Default title !!!')
		
	slug 			= models.SlugField(blank=True,unique=True)
	description 	= RichTextField()
	additional_info = RichTextField(blank=True,null=True)
	category 		= models.ManyToManyField(Category)
	# label			= models.CharField(choices=LABEL_CHOICES, max_length=1)
	visibility 		= models.IntegerField(choices=PRODUCT_VISIBILITY_CHOICES, verbose_name="Product's Visibility")
	
	status 			= models.IntegerField(choices=PRODUCT_STATUS_CHOICES, validators=[MinValueValidator(0), MaxValueValidator(2)])
	created 		= models.DateTimeField(auto_now_add=True)
	modified 		= models.DateTimeField(auto_now=True)
	created_by 		= models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="product_created_by", null=True,)
	modified_by 	= models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="product_modified_by", null=True,)
	history			= HistoricalRecords()

	def save(self, *args, **kwargs):
		#Saving the slug: if already exists then add random string with it
		if self.pk is None:
			self.slug = slugify(self.title)
			try:
				with transaction.atomic():
					super(Product, self).save(*args, **kwargs)
			except:
				ch = sr.choices(string.digits, k=2)
				ch += sr.choices(string.ascii_letters, k=3)
				sr.shuffle(ch)
				ch = ''.join(ch)
				self.slug = slugify(f"{self.title}-{ch}")
				try:
					super(Product, self).save(*args, **kwargs)
				except:
					self.save(*args, **kwargs)
     
	class Meta:
		ordering = ['-created']
		verbose_name_plural = 'Product'
	
	def __str__(self):
		return self.title

	def __unicode__(self):
	    return self.title


class Color(models.Model):
    name 				= models.CharField(max_length=20)
    code 				= models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""


class Size(models.Model):
    name 				= models.CharField(max_length=20)
    code 				= models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name


class Variants(models.Model):
    title 				= models.CharField(max_length=100, blank=True, null=True)
    product 			= models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', 
                                  related_query_name='variants',)
    color 				= models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    size 				= models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    # label			= models.CharField(choices=LABEL_CHOICES, max_length=1)
    is_display 			= models.BooleanField(default=False,blank=False, null=False,verbose_name="Is Display")
    is_treanding 		= models.BooleanField(default=False,blank=False, null=False,verbose_name="Is Display")
    
    image_galary		= models.ForeignKey("ImageGalary", blank=True, null=True, on_delete=models.CASCADE)
    price				= models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0),])
    discount_price		= models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[MinValueValidator(0),])
    
    created 		    = models.DateTimeField(auto_now_add=True)
    modified 		    = models.DateTimeField(auto_now=True)
    created_by 		    = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="variants_created_by", null=True,)
    modified_by 	    = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="variants_modified_by", null=True,)


    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Variants'

    def save(self, *args, **kwargs):
        
        if self.discount_price>self.price:
            
            raise ValueError("Discount price must be less than or equals to price")
        
        super().save(*args, **kwargs)
    
    def image_tag(self):
        try:
            img = Variants.objects.get(pk=self.pk).image_galary.cover
            if img.id is not None:
                return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
            else:
                return ""
        except:
            return ""
        
class ImageGalary(models.Model):
    title 			= models.CharField(max_length=50, blank=True)
    cover 			= models.ImageField(blank=True, upload_to='Products/%Y/%m/%d/')
    image1 			= models.ImageField(blank=True, upload_to='Products/%Y/%m/%d/')
    image2 			= models.ImageField(blank=True, upload_to='Products/%Y/%m/%d/')
    image3 			= models.ImageField(blank=True, upload_to='Products/%Y/%m/%d/')
    image4 			= models.ImageField(blank=True, upload_to='Products/%Y/%m/%d/')
    image5 			= models.ImageField(blank=True, upload_to='Products/%Y/%m/%d/')
 
    def __str__(self):
        return self.title

    def image_tag(self):
        try:
            img = ImageGalary.objects.get(pk=self.pk).cover
            if img.id is not None:
                return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
            else:
                return ""
        except:
            return ""
