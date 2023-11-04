from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager


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
    organizationPhone = models.CharField(max_length=13)
    organizationAddress = models.CharField(max_length=500)

    dateTimeStart = models.DateTimeField()
    dateTimeEnd = models.DateTimeField()
    letterFile = models.URLField()
    letterName = models.CharField(max_length=200, null=True)

    lotsInfo = models.TextField(null=True)

    moreInfo = models.URLField()

    def __str__(self):
        return self.tenderNum