# from django.db import models
#
#
#
# # Create your models here.
# class TendersList(models.Model):
#     tenderNum = models.BigIntegerField()
#     tenderName = models.CharField(max_length=500)
#     tenderFormat = models.CharField(max_length=100)
#     tenderSumm = models.BigIntegerField()
#     srok = models.IntegerField()
#
#     organizationName = models.CharField(max_length=500)
#     organizationPhone = models.CharField(max_length=13)
#     organizationAddress = models.CharField(max_length=500)
#
#     dateTimeStart = models.DateTimeField()
#     dateTimeEnd = models.DateTimeField()
#     letterFile = models.URLField()
#     letterName = models.CharField(max_length=200, null=True)
#
#     lotsInfo = models.TextField(null=True)
#
#     moreInfo = models.URLField()
#
#     def __str__(self):
#         return self.tenderNum