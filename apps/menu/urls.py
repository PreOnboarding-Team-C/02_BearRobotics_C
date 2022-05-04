from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.MenuListAPIView.as_view()),
    path('/<int:pk>', views.MenuDetailAPIView.as_view()),
]