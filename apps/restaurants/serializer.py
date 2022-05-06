from rest_framework.serializers import ModelSerializer, ReadOnlyField, SerializerMethodField

from apps.sales.models import Pos

from .models import Restaurant


class RestaurantSerializer(ModelSerializer):
    '''
    Assignee : 장우경
    Reviewer : 홍은비
    '''
    group_name = ReadOnlyField(source='group.name')

    class Meta:
        model = Restaurant
        fields = '__all__'


class RestraurantPaymentKPISerializer(ModelSerializer):
    count = ReadOnlyField()
    # window_size = ReadOnlyField()
    total_price = ReadOnlyField()
    hour = ReadOnlyField()
    day = ReadOnlyField()
    week = ReadOnlyField()
    month = ReadOnlyField()
    year = ReadOnlyField()


    class Meta:
        model = Pos
        # fields = ['restaurant_id', 'payment', 'total_price', 'count', 'hour']
        fields = ['restaurant_id', 'payment', 'total_price', 'count',  'hour', 'day', 'week', 'month', 'year']
        # fields = ['restaurant_id', 'payment', 'total_price', 'count', 'window_size']