from django.db import models
from schedule.models import Schedule
from django.utils.translation import gettext_lazy as _
from equipment.models import EquipmentType
# Create your models here.

FREQUENCY_CHOICES = [
    ('daily', 'Daily'),
    ('monthly', 'Monthly'),
]

class Package(models.Model):
    name = models.CharField(_("Name"),max_length=50, null=True,blank=True)
    price = models.IntegerField(_("Price"),null=True,blank=True)
    schedules = models.ManyToManyField(Schedule,blank=True)
    # start_time = models.TimeField(_("Start Time"),null=True,blank=True)
    # end_time = models.TimeField(_("End Time"),null=True,blank=True)
    equipmentType = models.ManyToManyField(EquipmentType,blank=True)
    desc = models.TextField(_("Description"),null=True,blank=True)
    frequency = models.CharField(_("Frequency"),max_length=50, null=True,blank=True,choices=FREQUENCY_CHOICES)

    def __str__(self) -> str:
        return f'{self.name} | {self.price} | {self.frequency}'
    
    def get_equipmentTypes(self):
        return self.equipmentType.all()
    
    def get_schedules(self):
        return self.schedules.all()