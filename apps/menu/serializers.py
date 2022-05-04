from dataclasses import field
from .models import Menu
from rest_framework import serializers


class MenuSerializer(serializers.ModelSerializer):
    """
        Asignee: 홍은비
        Reviewer: 진병수
    """
    class Meta:
        model = Menu
        fields = '__all__'
        
