from django.db import models
from django.utils import timezone

from user.models import Account

# Create your models here.


class Device(models.Model):
    device = models.CharField(max_length=100)
    account_id = models.ForeignKey(
        Account, related_name="device", on_delete=models.SET_NULL, null=True, blank=True)
    activation_date = models.DateTimeField(default=timezone.now)
    state = models.BooleanField(default=False)

    def __str__(self):
        return self.device
