# Generated by Django 2.2.4 on 2019-08-16 01:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('queuer', '0003_auto_20190815_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userqueue',
            name='number',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='user',
            field=models.ForeignKey(on_delete='models.CASCADE', related_name='wallet', to=settings.AUTH_USER_MODEL),
        ),
    ]