from .models import Pos
from rest_framework import serializers


class PosSerializer(serializers.ModelSerializer):
    """
        Asignee: 진병수
        Reviewer: 
    """
    class Meta:
        model = Pos
        fields = '__all__'