from django.db import models
from django.utils import timezone

from device.models import Device
from utils import getQuality

# Create your models here.


class Country(models.Model):
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.country

    @property
    def qualityAVG(self):
        data_item = self.city.all()
        total = sum([item.qualityAVG for item in data_item])
        return total


class City(models.Model):
    city = models.CharField(max_length=100)
    country_id = models.ForeignKey(
        Country, related_name="city", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.city

    @property
    def qualityAVG(self):
        data_item = self.district.all()
        total = sum([item.qualityAVG for item in data_item])
        return total


class District(models.Model):
    city_id = models.ForeignKey(
        City, related_name="district", on_delete=models.SET_NULL, null=True, blank=True)
    district = models.CharField(max_length=100)

    def __str__(self):
        return self.district

    @property
    def qualityAVG(self):
        data_item = self.data.all()
        total = sum([item.quality for item in data_item])
        return total


class Data(models.Model):
    district_id = models.ForeignKey(
        District, related_name='data', on_delete=models.CASCADE, null=True, blank=True)
    device_id = models.ForeignKey(
        Device, related_name='data', on_delete=models.CASCADE, null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    quality = models.IntegerField(default=0)
    difference_quality = models.IntegerField(default=0)
    date_time = models.DateTimeField('Date Time', null=True, blank=True)
    humidity = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    temperature = models.DecimalField(
        max_digits=6, decimal_places=2, default=0)
    warm = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    concentration = models.DecimalField(
        max_digits=6, decimal_places=2, default=0)
    smoke_sensor = models.BooleanField(default=False)
    methane_sensor = models.BooleanField(default=False)

    def __str__(self):
        return str(self.quality)

    def save(self, *args, **kwargs):
        self.quality = getQuality(self)
        lastQuality = Data.objects.filter(
            device_id=self.device_id).latest('date_time')
        self.difference_quality = self.quality - lastQuality.quality
        if self.date_time is None:
            self.date_time = timezone.now()
        return super(Data, self).save(*args, **kwargs)
