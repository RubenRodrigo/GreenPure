# Generated by Django 3.1.4 on 2021-10-14 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_auto_20211012_1828'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='date',
        ),
        migrations.RemoveField(
            model_name='data',
            name='time',
        ),
        migrations.AddField(
            model_name='data',
            name='date_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date'),
        ),
    ]