from datetime import datetime
from django.db.models import (
    Count, 
    DateTimeField, 
    CharField,
    Q,
    Count,
    Sum,
)
from django.db.models.functions import (
    Cast,
    Substr,
    TruncHour,
    TruncDay,
    TruncWeek, 
    TruncMonth, 
    TruncYear,
)
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.sales.models import Pos
from .models import Restaurant
from .serializer import RestaurantSerializer, RestaurantPaymentKPISerializer, PosSerializer


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


class RestaurantPaymentKPIView(APIView):
    '''
    Assignee : 홍은비
    Reviewer : 장우경, 진병수, 김수빈
    '''
    def get(self, request, pk):
        pos = Pos.objects.all()
        
        # Filter 1: Start Time / End Time
        
        start_time = request.GET.get('start_time', None)
        end_time = request.GET.get('end_time', None)

        if start_time and end_time:
            try:
                start_time = datetime.strptime(start_time, '%Y-%m-%d').date()
                end_time = datetime.strptime(end_time, '%Y-%m-%d').date()
                # end_time 은 포함되지 않아 icontains 조건을 추가해 임의로 포함시킴.
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
            pos = pos.annotate(hour=
                Substr(
                    Cast(TruncHour('created_datetime', output_field=DateTimeField()),
                        output_field=CharField()), 12, 2)
                    ).values('hour')\
                .annotate(count=Count('payment')).values('restaurant_id', 'payment', 'count', 'hour')

        elif window_size == 'DAY':
            pos = pos.annotate(day=
                Substr(
                    Cast(TruncDay('created_datetime', output_field=DateTimeField()),
                        output_field=CharField()), 9, 2)
                    ).values('day')\
                .annotate(count=Count('payment')).values('restaurant_id', 'payment', 'count', 'day')

        elif window_size == 'WEEK':
            pos = pos.annotate(window_size=TruncWeek('created_datetime')).values('window_size')\
                .annotate(count=Count('payment')).values('window_size', 'restaurant_id', 'payment', 'count')

        elif window_size == 'MONTH':
            pos = pos.annotate(month=
                Substr(
                    Cast(TruncMonth('created_datetime', output_field=DateTimeField()),
                        output_field=CharField()), 6, 2)
                    ).values('month')\
                .annotate(count=Count('payment')).values('restaurant_id', 'payment', 'count', 'month')
                
        elif window_size == 'YEAR':
            pos = pos.annotate(year=
                Substr(
                    Cast(TruncYear('created_datetime', output_field=DateTimeField()),
                        output_field=CharField()), 1, 4)
                    ).values('year')\
                .annotate(count=Count('payment')).values('restaurant_id', 'payment', 'count', 'year')

            
        serializer = RestaurantPaymentKPISerializer(pos, many=True)
        return Response(serializer.data, status=200)
