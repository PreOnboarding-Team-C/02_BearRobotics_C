from rest_framework import generics

from .models import Restaurant
from .serializer import RestaurantSerializer


class RestaurantListCreateView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    
    print(serializer_class)

    print('안 되나요??')
    