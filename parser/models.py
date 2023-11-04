from django.db import models

import companies.models


# Create your models here.
class TendersList(models.Model):
    tenderNum = models.BigIntegerField()
    tenderName = models.CharField(max_length=500)
    tenderFormat = models.CharField(max_length=100)
    tenderSumm = models.BigIntegerField()
    srok = models.IntegerField()

    organizationName = models.CharField(max_length=500)
    company_info = models.OneToOneField(
        companies.models.CompanyInfo,
        on_delete=models.CASCADE,
        related_name="tenders_list",
        null=True
    )
    organizationPhone = models.CharField(max_length=13)
    organizationAddress = models.CharField(max_length=500)

    dateTimeStart = models.DateTimeField()
    dateTimeEnd = models.DateTimeField()
    letterFile = models.URLField()
    letterName = models.CharField(max_length=200, null=True)

    lotsInfo = models.TextField(null=True)

    moreInfo = models.URLField()

    likes = models.PositiveIntegerField(default=0, null=True)
    dislikes = models.PositiveIntegerField(default=0, null=True)

    def save(self, *args, **kwargs):
        if not self.company_info:
            # Если связанный объект CompanyInfo отсутствует, создаем его
            company_info = companies.models.CompanyInfo(companyName=self.organizationName)
            company_info.save()
            self.company_info = company_info

        super().save(*args, **kwargs)

        self.company_info.likes = self.likes
        self.company_info.dislikes = self.dislikes
        self.company_info.save()

    def __str__(self):
        return self.tenderNum

