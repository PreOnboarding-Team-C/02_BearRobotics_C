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
from django.db.models.functions import  TruncWeek, TruncDate, ExtractHour, ExtractMonth, ExtractYear

import datetime

# def Date(str):
#     return datetime.datetime.strptime(str, '%Y-%m-%d').date()

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


# restaurants 는 FK 로 연결되어 있고
# menu 는 ManytoMany 로 연결되어 있습니다.
# 이 상태에서 해당 컬럼의 내용으로 어떻게 검색해서 보여줄 것인가?

class PosSearchAPIView(APIView):
    # Pos 객체 가져오기
    def get_object(self):
        try:
            return Pos.objects.all()
        except Pos.DoesNotExist:
            raise Http404

    def get(self, request):
        restaurant = request.GET.get('restaurant', None)
        menu       = request.GET.get('order_menu', None)
        num        = request.GET.get('number_of_party', None)
        payment    = request.GET.get('payment', None)
        min_price  = request.GET.get("min_price", None)
        max_price  = request.GET.get("max_price", None)

        q = Q()

        if restaurant:
            q &= Q(restaurant = restaurant)

        if menu:
            q &= Q(menu = menu)

        if num:
            q &= Q(number_of_party__number_of_party = num)

        if payment:
            q &= Q(payment = payment)

        if min_price:
            q &= Q(menu__price__gte=min_price)

        if max_price:
            q &= Q(menu__price__lte=max_price)

        
        objs = Pos.objects.filter(q)
        serializser = PosSearchSerializer(objs, many=True)
        return Response(serializser.data, status=status.HTTP_200_OK)