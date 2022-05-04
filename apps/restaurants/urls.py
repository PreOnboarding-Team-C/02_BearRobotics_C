from django.urls import path

from .views import RestaurantListCreateView


urlpatterns = [
    path('', RestaurantListCreateView.as_view()),
]