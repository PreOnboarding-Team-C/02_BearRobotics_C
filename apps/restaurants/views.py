from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.sales.models import Pos
from .models import Restaurant
from .serializer import RestaurantSerializer, RestraurantPaymentKPISerializer
from datetime import datetime
from django.db.models.functions import TruncHour, TruncWeek, TruncDay, TruncMonth, TruncYear
from django.db.models import Count, Q, Sum

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


class RestaurantPaymentKPIView(APIView):
    def get(self, request, pk):
        pos = Pos.objects.filter(restaurant_id=pk)

        if not pos:
            return Response('해당 레스토랑의 pos 사용 이력이 존재하지 않습니다.', status=404)

        
        # Filter 1: Start time/ End time

        start_time = request.GET.get('start_time', None)
        end_time = request.GET.get('end_time', None)
        if start_time and end_time:
            try:
                start_time = datetime.strptime(start_time, '%Y-%m-%d').date()
                end_time = datetime.strptime(end_time, '%Y-%m-%d').date()
                pos = pos.filter(Q(created_datetime__range=(start_time,end_time)) | Q(created_datetime__icontains=end_time))
            except ValueError:
                return Response('[날짜 형식 오류] 날짜를 yyyy-mm-dd 형식으로 요청해주십시오.', status=404)


        # Filter 2: Price range

        min_price = request.GET.get('min_price', None)
        max_price = request.GET.get('max_price', None)

        if min_price and max_price:
            pos = pos.annotate(total_price=Sum('menu__price')).values('id', 'total_price')\
                .filter(total_price__gte=min_price, total_price__lte=max_price)


        # Filter 3: Number of party

        min_party = request.GET.get('min_party', None)
        max_party = request.GET.get('max_party', None)
        if min_party and max_party:
            pos = pos.filter(number_of_party__gte=min_party, number_of_party__lte=max_party)


        # Filter 4: Restaurant group

        group = request.GET.get('group', None)
        if group:
            pos = pos.filter(restaurant__group__name=group)

        # HOUR, DAY, WEEK, MONTH, YEAR

        window_size = request.GET.get('window_size', None)
        window_type = ['HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR']

        if not window_size in window_type:
            return Response('[window size 타입 오류] window size는 HOUR, DAY, WEEK, MONTH, YEAR 중 하나여야합니다.', status=404)

        if window_size == 'HOUR':
            pos = pos.annotate(window_size=TruncHour('created_datetime')).values('window_size')\
                .annotate(count=Count('payment')).values('window_size', 'payment', 'count')
            print(pos)
        elif window_size == 'DAY':
            pos = pos.annotate(window_size=TruncDay('created_datetime')).values('window_size')\
                .annotate(count=Count('payment')).values('window_size', 'payment', 'count')
        elif window_size == 'WEEK':
            pos = pos.annotate(window_size=TruncWeek('created_datetime')).values('window_size')\
                .annotate(count=Count('payment')).values('window_size', 'payment', 'count')
        elif window_size == 'MONTH':
            pos = pos.annotate(window_size=TruncMonth('created_datetime')).values('window_size')\
                .annotate(count=Count('payment')).values('window_size', 'payment', 'count')
        elif window_size == 'YEAR':
            pos = pos.annotate(window_size=TruncYear('created_datetime')).values('window_size')\
                .annotate(count=Count('payment')).values('window_size', 'payment', 'count')

        serializer = RestraurantPaymentKPISerializer(pos, many=True)
        return Response(serializer.data, status=200)