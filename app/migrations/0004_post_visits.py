# Generated by Django 3.1.7 on 2021-03-19 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210318_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='visits',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
