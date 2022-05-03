from django.db import models

from apps.restaurants.models import Restaurant


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'menu'
