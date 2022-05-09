from urllib import response
from django.shortcuts import render

# 데이터 처리
from apps.sales.models import Pos
from apps.sales.serializers import PosSerializer, PosSearchSerializer

# APIView를 사용하기 위해 import
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from django.db.models import Q, F, Sum, Count
from django.db.models import DateField, DateTimeField, CharField
from django.db.models.functions import TruncHour, TruncWeek, TruncDay, TruncMonth, TruncYear, Cast, Substr

import datetime

# Create your views here.
# Pos의 목록을 보여주는 역할
class PosListAPIView(APIView):
    '''
    Assignee : 진병수
    Reviewer : 
    '''
    # Pos list를 보여줄 때
    def get(self, request):
        Poses = Pos.objects.all()
        # 여러 개의 객체를 serialization하기 위해 many=True로 설정
        serializer = PosSerializer(Poses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 새로운 Pos를 생성할 때
    def post(self, request):
        # request.data는 사용자의 입력 데이터
        serializer = PosSerializer(data=request.data)
        if serializer.is_valid(): #유효성 검사
            serializer.save() # 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Pos의 detail을 보여주는 역할
class PosDetailAPIView(APIView):
    '''
    Assignee : 진병수
    Reviewer : 
    '''
    # Pos 객체 가져오기
    def get_object(self, pk):
        try:
            return Pos.objects.get(pk=pk)
        except Pos.DoesNotExist:
            raise Http404
    
    # 특정 Pos의 detail 보기
    def get(self, request, pk, format=None):
        pos = self.get_object(pk)
        serializer = PosSerializer(pos)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # 특정 Pos의 deatail 수정하기
    def patch(self, request, pk, format=None):
        pos = self.get_object(pk)
        serializer = PosSerializer(pos, data=request.data, partial=True) 

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 특정 Pos 삭제하기
    def delete(self, request, pk, format=None):
        pos = self.get_object(pk)
        pos.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)   


class PosSearchAPIView(APIView):
    '''
    Assignee : 진병수
    Reviewer : 
    '''

    # Pos 객체 가져오기
    def get_object(self):
        try:
            return Pos.objects.all()
        except Pos.DoesNotExist:
            raise Http404

    def get(self, request):
        restaurant = request.GET.get('restaurant', None)
        group      = request.GET.get('group')

        menu       = request.GET.get('order_menu', None)
        payment    = request.GET.get('payment', None)

        start_time = request.GET.get('start_time')
        end_time   = request.GET.get('end_time', None)
        
        min_price  = request.GET.get("min_price", None)
        max_price  = request.GET.get("max_price", None)

        min_party  = request.GET.get("min_party", None)
        max_party  = request.GET.get("max_party", None)

        if start_time and end_time:
            try:
                start_time = datetime.strptime(start_time, '%Y-%m-%d').date()
                end_time = datetime.strptime(end_time, '%Y-%m-%d').date()
                pos = pos.filter(Q(created_datetime__range=(start_time,end_time)) | Q(created_datetime__icontains=end_time))
            except ValueError:
                return Response('[날짜 형식 오류] 날짜를 yyyy-mm-dd 형식으로 요청해주십시오.', status=404)

        q = Q()

        if restaurant:
            q &= Q(restaurant = restaurant)

        if group:
            q &= Q(restaurant__group = group)

        if menu:
            q &= Q(menu = menu)

        if payment:
            q &= Q(payment = payment)

        if min_price:
            q &= Q(menu__price__gte = min_price)

        if max_price:
            q &= Q(menu__price__lte = max_price)

        if min_party:
            q &= Q(menu__price__gte = min_price)

        if max_party:
            q &= Q(menu__price__lte = max_price)

        pos = Pos.objects.all()
            
        # 필터1 : window_size 으로 (HOUR, DAY, WEEK, MONTH, YEAR) - 필수★★
        window_size = request.GET.get('window_size', None)
        window_type = ['HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR']

        if not window_size in window_type:
            return Response('[window size 타입 오류] window size는 HOUR, DAY, WEEK, MONTH, YEAR 중 하나여야합니다.', status=404)

        if window_size == 'HOUR':
            pos = (
                    pos
                    .annotate(hour=
                        Substr(
                            Cast(TruncHour(
                                'created_datetime', 
                                output_field=DateTimeField()),
                                output_field=CharField()), 12, 2))
                                .values('hour')
                                .annotate(count=Count('id'))
                                .values('restaurant_id', 'payment', 'count', 'hour')
                )

        elif window_size == 'DAY':
            pos = (
                    pos
                    .annotate(day=
                        Substr(
                            Cast(TruncDay(
                                'created_datetime',
                                output_field=DateTimeField()),
                                output_field=CharField()), 9, 2))
                                .values('day')
                                .annotate(count=Count('id'))
                                .values('restaurant_id', 'payment', 'count', 'day')
                )

        elif window_size == 'WEEK':
            pos = (
                    pos
                    .annotate(window_size=
                        TruncWeek('created_datetime'))
                        .values('window_size')
                        .annotate(count=Count('id'))
                        .values('window_size', 'restaurant_id', 'payment', 'count')
                )

        elif window_size == 'MONTH':
            pos = (
                    pos
                    .annotate(month=
                        Substr(
                            Cast(TruncMonth(
                                'created_datetime',
                                output_field=DateTimeField()),
                                output_field=CharField()), 6, 2)
                                ).values('month')
                                .annotate(count=Count('id'))
                                .values('restaurant_id', 'payment', 'count', 'month')
                )

        elif window_size == 'YEAR':
            pos = (
                    pos
                    .annotate(year=
                        Substr(
                            Cast(TruncYear(
                                'created_datetime', 
                                output_field=DateTimeField()),
                                output_field=CharField()), 1, 4)
                                ).values('year')
                                .annotate(count=Count('id'))
                                .values('restaurant_id', 'payment', 'count', 'year')
                )


        # 필터2 : 날짜 범위로
        if start_time and end_time:
            if start_time > end_time:
                return Response({"message" : "날짜를 다시 확인하세요."}, status=status.HTTP_400_BAD_REQUEST)

            if ValueError:
                return Response('[날짜 형식 오류] 날짜를 yyyy-mm-dd 형식으로 요청해주십시오.', status=404)

            q &= Q(created_datetime__range=(start_time,end_time)) | Q(created_datetime__icontains=end_time) # 합집합개념

            q &= Q(created_datetime__range=(start_time,end_time))

            pos = (
                Pos
                .objects
                .filter(q)
                .annotate(date = window_type[window_size])
                .values('created_datetime')
                )

        
        # 필터3 : total_price 범위로 (최소 총 금액 : min_price ~ 최대 총 금액 : max_price)
        if min_price and max_price:
            if max_price is None:
                return Response({"message" : "가격을 다시 확인하세요."}, status=status.HTTP_400_BAD_REQUEST)
            
            q &= Q(price__range = [min_price, max_price])

            pos = (
                pos
                .annotate(total_price=Sum('menu__price'))
                .values('id', 'created_datetime', 'restaurant__name', 'total_price')
                .filter(total_price__gte=min_price, total_price__lte=max_price)
                )


        # 필터4 : number_of_party 범위로
        if min_party and max_party:

            q &= Q(number_of_party__range = [min_party, max_party])

            pos = (
                pos
                .annotate(total_price = Sum('menu__price'))
                .values(
                    'id',
                    'created_datetime',
                    'number_of_party',
                    'total_price')
                .filter(number_of_party__gte=min_party, number_of_party__lte=max_party)
                )

        return Response(pos, status=status.HTTP_200_OK)