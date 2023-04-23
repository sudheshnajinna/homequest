from django.contrib import admin

# Register your models here.
from .models import Apartment
from .models import Wishlist

admin.site.register(Apartment)
admin.site.register(Wishlist)