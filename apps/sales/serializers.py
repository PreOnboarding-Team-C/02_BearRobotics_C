from apps.sales.models import Pos
from apps.restaurants.serializer import RestaurantSerializer
from apps.menu.serializers import MenuSerializer

from rest_framework import serializers


class PosSerializer(serializers.ModelSerializer):
    """
    Asignee : 진병수
    Reviewer :
    """

    # menu = MenuSerializer(source='menu.name', many=True)
    # print(f"menu 입니다 {menu}")

    class Meta:
        model = Pos

        fields = '__all__'
    

class PosSearchSerializer(PosSerializer):
    """
    Asignee : 진병수
    Reviewer : 
    """
    restaurant = serializers.ReadOnlyField(source='restaurant.name')
    menu_info = MenuSerializer(source='menu', many=True, read_only=True)
    count = serializers.ReadOnlyField()
    # menu = MenuSerializer(source='pos_menu.id', many=True)

    # print(f"menu 입니다 : {menu}")
    # pos = Pos.objects.get(pk=1)
    # temp = pos.menu_set_all()

    class Meta:
        model = Pos
        
        fields = '__all__'