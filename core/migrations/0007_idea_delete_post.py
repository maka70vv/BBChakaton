# Generated by Django 4.2.6 on 2023-11-05 05:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        ('core', '0006_remove_contractslist_totalpricecontract'),
    ]

    operations = [
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]