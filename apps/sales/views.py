from django.shortcuts import render

# Create your views here.
# 데이터 처리
from .models import Pos
from .serializers import PosSerializer

# APIView를 사용하기 위해 import
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

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
        return Response(serializer.data)

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

        return Response(serializer.data)

    # 특정 Pos의 deatail 수정하기
    def put(self, request, pk, format=None):
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
    