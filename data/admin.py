from django.contrib import admin

from data.models import City, Country, Data, District

# Register your models here.

admin.site.register(Data)
admin.site.register(District)
admin.site.register(City)
admin.site.register(Country)
