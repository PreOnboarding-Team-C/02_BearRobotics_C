from django.db import models

from apps.restaurants.models import Restaurant
from apps.menu.models import Menu
from utils.time_stamp import TimeStampModel


class Pos(TimeStampModel):
    '''
    Assignee : 장우경
    Reviewer : 홍은비, 진병수, 김수빈
    '''
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu = models.ManyToManyField(Menu)
    number_of_party = models.PositiveSmallIntegerField()
    payment = models.CharField(max_length=30)
    
    class Meta:
        verbose_name_plural = "POS목록"
        db_table = 'pos'

    def __str__(self) -> str:
        return self.restaurant