# Generated by Django 4.2.6 on 2023-11-04 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyinfo',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
