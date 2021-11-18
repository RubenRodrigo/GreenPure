from django.contrib import admin

from device.models import Device

# Register your models here.


class DeviceAdmin(admin.ModelAdmin):
    readonly_fields = ('unique_id',)


admin.site.register(Device, DeviceAdmin)
