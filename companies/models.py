from django.db import models


# Create your models here.
class CompanyInfo(models.Model):
    companyName = models.CharField(max_length=500)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def update_likes_dislikes(self, likes, dislikes):
        self.likes += likes
        self.dislikes += dislikes
        self.save()

    @classmethod
    def update_likes_dislikes_by_company_name(cls, company_name, likes, dislikes):
        company_info = cls.objects.filter(companyName=company_name)
        if company_info:
            company_info.update_likes_dislikes(likes, dislikes)

    def __str__(self):
        return self.companyName
