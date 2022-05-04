from django.db import models

from utils.time_stamp import TimeStampModel


class Group(models.Model):
    '''
    Assignee : 장우경
    Reviewer : 홍은비, 진병수, 김수빈
    '''
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'groups'


class Restaurant(TimeStampModel):
    '''
    Assignee : 장우경
    Reviewer : 홍은비, 진병수, 김수빈
    '''
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'restaurants'
