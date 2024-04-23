from django.db import models

# Create your models here.


class DataSet(models.Model):
    name = models.CharField(max_length=100,default="DatasetStatistic")

class Statistic(models.Model):
    col_name = models.CharField(max_length=100)
    stat_name = models.CharField(max_length=100)
    value = models.FloatField(default=0)
    data_set = models.ForeignKey(DataSet, related_name='statistics', on_delete=models.CASCADE)