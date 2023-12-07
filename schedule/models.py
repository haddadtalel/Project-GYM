from django.db import models
from django.utils.translation import gettext_lazy as _

DAY_CHOICES = [
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
]
TYPE_CHOICE = [
    ('coach', 'Coach'),
    ('stuff', 'Stuff'),
    ('member', 'Member'),
    ('package', 'Package'),
]

# Create your models here.
class Schedule(models.Model):
    name = models.CharField(_("Name"),max_length=50, null=True,blank=True,choices=TYPE_CHOICE)
    day = models.CharField(_("Day"),max_length=10, choices=DAY_CHOICES,null=True,blank=True)
    start_time = models.TimeField(_("Start Time"),null=True,blank=True)
    end_time = models.TimeField(_("End Time"),null=True,blank=True)

    def __str__(self) -> str:
        return f'{self.day} | {self.start_time} - {self.end_time} for {self.name}'