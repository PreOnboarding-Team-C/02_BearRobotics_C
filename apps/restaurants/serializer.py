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


class PosSerializer(RestaurantSerializer):
    '''
    Assignee : 장우경
    Reviewer : -
    '''
    group_id = ReadOnlyField(source='restaurant__group')
    count = ReadOnlyField(source='num_count')
    
    class Meta:
        model = Pos
        fields = ['number_of_party', 'restaurant_id', 'group_id', 'count']


class RestaurantPaymentKPISerializer(ModelSerializer):
    '''
    Assignee : 홍은비
    Reviewer : 김수빈
    '''
    count = ReadOnlyField()
    total_price = ReadOnlyField()
    hour = ReadOnlyField()
    day = ReadOnlyField()
    week = ReadOnlyField()
    month = ReadOnlyField()
    year = ReadOnlyField()

    class Meta:
        model = Pos
        fields = ['restaurant_id', 'payment', 'total_price', 'count',  'hour', 'day', 'week', 'month', 'year']
