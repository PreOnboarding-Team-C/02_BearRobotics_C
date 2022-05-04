from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin', admin.site.urls),
    path('api/v1/restaurants', include('apps.restaurants.urls')),
    # path('api/v1', include('apps.sales.urls')),
]
