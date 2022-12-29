from django.db import models


class DroneScannerInfo(models.Model):
    deviceId = models.CharField(max_length=50)
    listenRange = models.FloatField()
    deviceStarted = models.DateTimeField(blank=True, null=True)
    uptimeSeconds = models.IntegerField()
    updateIntervalMs = models.IntegerField()
    time_added = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return '%s' % (self.deviceId)

class PilotData(models.Model):
    pilotId = models.CharField(max_length=20, blank=True, null=True)
    firstName = models.CharField(max_length=20, blank=True, null=True)
    lastName = models.CharField(max_length=20, blank=True, null=True)
    phoneNumber = models.CharField(max_length=15, blank=True, null=True)
    createdDt = models.DateTimeField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    time_added = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return '%s' % (self.pilotId)

class DroneData(models.Model):
    serialNumber = models.CharField(max_length=20)
    model = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=50)
    mac = models.CharField(max_length=17)
    ipv4 = models.CharField(max_length=15)
    ipv6 = models.CharField(max_length=40)
    firmware = models.CharField(max_length=10)
    positionY = models.FloatField()
    positionX = models.FloatField()
    altitude = models.FloatField()
    pilot = models.ForeignKey(PilotData, related_name='pilot', on_delete=models.PROTECT)
    time_added = models.DateTimeField(blank=True, null=True)
    snapshotTimestamp = models.DateTimeField(blank=True, null=True)
    device = models.ForeignKey(DroneScannerInfo, related_name='device', on_delete=models.PROTECT, blank=True, null=True)


    def __str__(self):
        return '%s' % (self.serialNumber)

