from django.contrib import admin
from data.models import Data

from device.models import Device

# Register your models here.


class DataInline(admin.TabularInline):
    model = Data


class DeviceAdmin(admin.ModelAdmin):
    readonly_fields = ('unique_id',)
    inlines = [
        DataInline,
    ]


admin.site.register(Device, DeviceAdmin)
