from django.urls import path

from .views import RestaurantListAPIView, RestaurantDetailAPIView


urlpatterns = [
    path('', RestaurantListAPIView.as_view()),
    path('/<int:pk>', RestaurantDetailAPIView.as_view()),
]
