from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin', admin.site.urls),
    path('api/v1/menu', include('apps.menu.urls')),
    path('api/v1/restaurants', include('apps.restaurants.urls')),
    path('api/v1/pos', include('apps.sales.urls')),
]
