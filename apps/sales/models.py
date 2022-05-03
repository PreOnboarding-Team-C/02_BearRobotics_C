from django.db import models
from apps.restaurants.models import Restaurant
from utils.time_stamp import TimeStampModel


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'menus'


class Pos(TimeStampModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu = models.ManyToManyField(Menu)
    number_of_party = models.PositiveSmallIntegerField()
    payment = models.CharField(max_length=30)
    
    class Meta:
        db_table = 'pos'
