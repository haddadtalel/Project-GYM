from django.db import models
from schedule.models import Schedule
from django.utils.translation import gettext_lazy as _
# Create your models here.

class EquipmentType(models.Model):
    name = models.CharField(_("Name"),max_length=50, null=True,blank=True)

    def __str__(self) -> str:
        return self.name

class Equipment(models.Model):
    name = models.CharField(_("Name"),max_length=50, null=True,blank=True)
    equipmentType = models.ManyToManyField(EquipmentType,blank=True)
    maintenanceDate = models.DateField(_("Maintenance Date"), null=True,blank=True)
    is_available =  models.BooleanField(_("Availability Status"),default=True)
    url =  models.TextField(_("Url"),null=True,blank=True)

    def __str__(self) -> str:
        return f'{self.name}'

class EquipmentActivityTrack(models.Model):
    start_time = models.DateField(_("Booking start"),null=True,blank=True)
    end_time = models.DateField(_("Booking end"),null=True,blank=True)
    # booked_by = 
    # booked_for =
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.equipment} | {self.start_time} - {self.end_time}'