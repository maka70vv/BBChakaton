from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

from companies.models import CompanyInfo
# from core.calculatePriceContract import calculate_price


class Post(models.Model):
    h1 = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = RichTextUploadingField()
    content = RichTextUploadingField()
    image = models.ImageField()
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()

    def __str__(self):
        return self.title


class TendersList(models.Model):
    tenderNum = models.BigIntegerField()
    tenderName = models.CharField(max_length=500)
    tenderFormat = models.CharField(max_length=100)
    tenderSumm = models.BigIntegerField()
    srok = models.IntegerField()

    organizationName = models.CharField(max_length=500)
    company_info = models.ForeignKey(
        CompanyInfo,
        on_delete=models.CASCADE,
        related_name="tenders_list",
        null=True
    )
    organizationPhone = models.CharField(max_length=13)
    organizationAddress = models.CharField(max_length=500)

    dateTimeStart = models.DateTimeField()
    dateTimeEnd = models.DateTimeField(null=True)
    letterFile = models.URLField(null=True)
    letterName = models.CharField(max_length=200, null=True)

    lotsInfo = models.TextField(null=True)

    moreInfo = models.URLField()

    likes = models.PositiveIntegerField(default=0, null=True)
    dislikes = models.PositiveIntegerField(default=0, null=True)

    def save(self, *args, **kwargs):
        current_time = timezone.now()

        if self.dateTimeEnd < current_time and self.dateTimeEnd:
            # Если время окончания тендера раньше текущего времени, удаляем объект
            self.delete()
            return
        if not self.company_info:
            # Ищем компанию по имени
            existing_company = CompanyInfo.objects.filter(companyName=self.organizationName).first()

            if existing_company:
                # Если компания существует, используем ее
                self.company_info = existing_company
            else:
                # Если компания не существует, создаем новую
                new_company_info = CompanyInfo(companyName=self.organizationName)
                new_company_info.save()
                self.company_info = new_company_info

        CompanyInfo.update_likes_dislikes_by_company_name(self.organizationName, self.likes,
                                                                           self.dislikes)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.tenderNum


class ContractsList(models.Model):
    tenderNum = models.BigIntegerField()
    tenderName = models.CharField(max_length=500)

    winnerName = models.CharField(max_length=500)
    company_info = models.ForeignKey(
        CompanyInfo,
        on_delete=models.CASCADE,
        related_name="contracts_list",
        null=True
    )

    dateContract = models.DateField()
    contractNum = models.CharField(max_length=100)

    lotsInfo = models.TextField()
    pricesOnTender = models.TextField()
    pricesOnContract = models.TextField()

    likes = models.PositiveIntegerField(default=0, null=True)
    dislikes = models.PositiveIntegerField(default=0, null=True)

    def save(self, *args, **kwargs):
        if not self.company_info:
            # Ищем компанию по имени
            existing_company = CompanyInfo.objects.filter(companyName=self.winnerName).first()

            if existing_company:
                # Если компания существует, используем ее
                self.company_info = existing_company
            else:
                # Если компания не существует, создаем новую
                new_company_info = CompanyInfo(companyName=self.winnerName)
                new_company_info.save()
                self.company_info = new_company_info

        # self.totalPriceContract = calculate_price(self.pricesOnContract)

        CompanyInfo.update_likes_dislikes_by_company_name(self.winnerName, self.likes, self.dislikes)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.tenderNum
