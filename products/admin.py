from django.contrib import admin
from .models import Product, Category, Color, Size, Variants, ImageGalary


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Variants)
admin.site.register(ImageGalary)