from django.db import models

class Vehicle(models.Model):
    vehicle_id = models.CharField(max_length=36, primary_key=True)
    user_id = models.CharField(max_length=100, null=True, blank=True)  # allow nulls
    vehicle_name = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)  # fix for migrations
    year = models.IntegerField(null=True, blank=True)

class MaintenanceRecord(models.Model):
    record_id = models.CharField(max_length=36, primary_key=True)
    vehicle_id = models.CharField(max_length=36, null=True, blank=True)  # fixing this too
    service_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
