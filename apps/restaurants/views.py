from datetime import datetime
from django.db.models import Count
from rest_framework import generics, status
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response

from apps.sales.models import Pos
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


# Restaurant별 일행 수에 따른 KPI
class KPIPerRestaurantAPIView(APIView):
    '''
    Assignee : 장우경
    Reviewer : 홍은비, 진병수
    '''
    def get(self, request):
        try:
            start_time = datetime.strptime(request.GET.get('start_time', None), '%Y-%m-%d').date()
            end_time = datetime.strptime(request.GET.get('end_time', None), '%Y-%m-%d').date()
        except TypeError:
            return Response({'message': '날짜를 입력해주세요'}, status=status.HTTP_404_NOT_FOUND)
        min_party = request.GET.get('min_party', None)
        max_party = request.GET.get('max_party', None)
        group_id = request.GET.get('group_id', None)
        # min_price = request.GET.get('min_price', None)
        # max_price = request.GET.get('max_price', None)
        
        q = Q()
    
        # 시간 지정하여 조회    
        if start_time and end_time:
            q &= Q(created_datetime__gte=start_time, created_datetime__lte=end_time)
    
        # 인원별 조회
        if min_party and max_party:
            q &= Q(number_of_party__gte=min_party, number_of_party__lte=max_party)

        # 그룹별 조회
        if group_id:
            q &= Q(restaurant__group=group_id)
    
        pos_queryset = Pos.objects.filter(q).values('number_of_party')\
                        .annotate(num_count=Count('number_of_party'))\
                        .values('restaurant_id', 'number_of_party', 'num_count', 'restaurant__group')
    
        serializer = PosSerializer(pos_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
