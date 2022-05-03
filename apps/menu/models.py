from django.db import models

from apps.restaurants.models import Restaurant


class Menu(models.Model):
    '''
    Assignee : 장우경
    Reviewer : 홍은비, 진병수, 김수빈
    '''
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'menus'
