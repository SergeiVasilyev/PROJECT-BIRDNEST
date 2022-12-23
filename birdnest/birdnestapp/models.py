from django.db import models



class PilotData(models.Model):
    pilotId = models.CharField(max_length=20)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    phoneNumber = models.CharField(max_length=15)
    createdDt = models.DateField()
    email = models.EmailField()
    
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
    pilot = models.ForeignKey(PilotData, on_delete=models.PROTECT)

    def __str__(self):
        return '%s' % (self.serialNumber)

