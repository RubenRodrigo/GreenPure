from django.utils import timezone
from django.conf import settings


def getQuality(data):
    quality = 1
    if data.temperature <= 26 and data.temperature >= 15:
        quality += 0
    elif data.temperature < 15 and data.temperature >= 5:
        quality += 10
    else:
        quality += 20

    if data.humidity <= 65 and data.humidity >= 55:
        quality += 0
    elif data.humidity < 55 and data.humidity >= 40:
        quality += 10
    else:
        quality += 20

    if data.methane_sensor:
        quality += 30
    else:
        quality += 0

    if data.smoke_sensor:
        quality += 20
    else:
        quality += 0

    return quality


def get_filter_by_date(filter_by):
    if filter_by is not None:
        if filter_by in settings.FILTER_OPTIONS:
            time_threshold = timezone.now() - timezone.timedelta(hours=int(filter_by))
            return time_threshold
        return timezone.now() - timezone.timedelta(hours=1)

    return timezone.now() - timezone.timedelta(hours=1)
