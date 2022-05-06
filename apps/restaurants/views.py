from datetime import datetime
from django.db.models import Count
from rest_framework import generics, status
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response

from apps.sales.models import Pos
from apps.restaurants.models import Group
from .models import Restaurant
from .serializer import PosSerializer, RestaurantSerializer


# Restaurnat 데이터 생성 및 전체 리스트 조회 API
class RestaurantListAPIView(generics.ListCreateAPIView):
    '''
    Assignee : 장우경
    Reviewer : 홍은비
    '''
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


# Restaurnat 상세 정보 조회, 수정(업데이트), 삭제 API
class RestaurantDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Assignee : 장우경
    Reviewer : -
    '''
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class KPIPerRestaurantAPIView(APIView):
    '''
    Assignee : 장우경
    Reviewer : 홍은비, 진병수
    '''
    def get(self, request):
        start_time = datetime.strptime(request.GET.get('start_time', None), '%Y-%m-%d').date()
        end_time = datetime.strptime(request.GET.get('end_time', None), '%Y-%m-%d').date()
        
        min_price = request.GET.get('min_price', None)
        max_price = request.GET.get('max_price', None)
        number_of_party = request.GET.get('number_of_party', None)
        group_id = request.GET.get('group_id', None)
    
        # pos_time = Pos.objects.filter(created_datetime__range=[start_time, end_time])
        # print(pos_time)
        
        q = Q()
        
        if min_price:
            q &= Q(menu__price__gte=min_price)
            
        if max_price:
            q &= Q(menu__price__lte=max_price)
            
        if number_of_party:
            q &= Q(number_of_party=number_of_party)
            
        if group_id:
            q &= Q(restaurant__group=group_id)
        
        if start_time:
            q &= Q(created_datetime__gte=start_time)
        
        if end_time:
            q &= Q(created_datetime__lte=end_time)
        
        pos_queryset = Pos.objects.filter(q).values('number_of_party').annotate(num_count=Count('number_of_party')).values('restaurant', 'number_of_party', 'num_count', 'restaurant_id__group')
        print(pos_queryset)
        
        serializer = PosSerializer(pos_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
