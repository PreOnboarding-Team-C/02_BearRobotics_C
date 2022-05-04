from django.contrib import admin
from apps.restaurants.models import Group, Restaurant
# Register your models here.

admin.site.register([Group, Restaurant])

