from rest_framework.serializers import ModelSerializer, ReadOnlyField

from .models import Group, Restaurant


class RestaurantSerializer(ModelSerializer):
    group_name = ReadOnlyField(source='group.name')

    class Meta:
        model = Restaurant
        fields = '__all__'
        # fields = ['name', 'city', 'address', 'group']
