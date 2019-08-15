# Generated by Django 2.2.4 on 2019-08-15 14:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('queuer', '0002_wallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='latest_assigned',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='UserQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('queue', models.ForeignKey(on_delete='models.CASCADE', to='queuer.Queue')),
                ('user', models.ForeignKey(on_delete='models.CASCADE', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
