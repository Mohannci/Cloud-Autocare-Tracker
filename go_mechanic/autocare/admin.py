from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Vehicle, MaintenanceRecord

admin.site.register(Vehicle)
admin.site.register(MaintenanceRecord)