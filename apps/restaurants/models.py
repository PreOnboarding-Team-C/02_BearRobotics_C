from django.db import models

from utils.time_stamp import TimeStampModel


class Group(models.Model):
    name = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'groups'


class Restaurant(TimeStampModel):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'restaurants'
