# Generated by Django 3.1.4 on 2021-10-28 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_auto_20211014_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='difference_quality',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='data',
            name='date_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date Time'),
        ),
    ]
