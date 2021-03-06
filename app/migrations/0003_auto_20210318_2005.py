# Generated by Django 3.1.7 on 2021-03-18 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210318_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='answercategory',
            name='answer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='reviewed_categories', to='app.answer'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='answercategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_categories', to='app.category'),
        ),
    ]
