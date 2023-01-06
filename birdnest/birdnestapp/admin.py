from django.contrib import admin
from .models import PilotData, DroneData, DroneScannerInfo



@admin.register(DroneScannerInfo)
class DroneScannerInfoAdmin(admin.ModelAdmin):
    list_display = ['deviceId', 'listenRange', 'deviceStarted', 'uptimeSeconds', 'updateIntervalMs', 'time_added']

@admin.register(PilotData)
class PilotDataAdmin(admin.ModelAdmin):
    list_display = ['pilotId', 'firstName', 'lastName', 'phoneNumber', 'createdDt', 'email']

@admin.register(DroneData)
class DroneDataAdmin(admin.ModelAdmin):
    list_display = ['serialNumber', 'model', 'manufacturer', 'mac', 'ipv4', 'ipv6', 'firmware', 'positionY', 'positionX', 'altitude', 'pilot']

