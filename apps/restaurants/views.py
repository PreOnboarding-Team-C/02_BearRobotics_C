from rest_framework import generics

from .models import Restaurant
from .serializer import RestaurantSerializer


class RestaurantListAPIView(generics.ListCreateAPIView):
    '''
    Assignee : 장우경
    Reviewer : 홍은비
    '''
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Assignee : 장우경
    Reviewer : -
    '''
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
