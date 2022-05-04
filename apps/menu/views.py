from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from .serializers import MenuSerializer
from rest_framework.response import Response
from .models import Menu


class MenuListAPIView(APIView):
    """
        Asignee: 홍은비
        Reviewer: 장우경
    """
    def get(self, request):
        serializer = MenuSerializer(Menu.objects.all(), many=True)
        return Response(serializer.data, status=200)
    
    def post(self, request):
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class MenuDetailAPIView(APIView):
    """
        Asignee: 홍은비
        Reviewer: 장우경
    """
    def get_object(self, pk):
        return get_object_or_404(Menu, pk=pk)
    
    def get(self, request, pk):
        menu = self.get_object(pk)
        serializer = MenuSerializer(menu)
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        menu = self.get_object(pk)
        serializer = MenuSerializer(menu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, pk):
        menu = self.get_object(pk)
        menu.delete()
        return Response(status=204)
