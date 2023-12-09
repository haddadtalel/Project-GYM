from django.db import models
from django.utils.translation import gettext_lazy as _
from schedule.models import Schedule

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
]

# Create your models here.
class Coach(models.Model):
    coachId = models.CharField(_("Coach Id"),max_length=20,null=True,blank=True)
    name = models.CharField(_("Full Name"),max_length=50,null=True,blank=True)
    phone = models.CharField(_("Phone"),unique=True,max_length=11,blank=True,null=True)
    dob = models.DateField(_("Date of Birth"),null=True,blank=True)
    
    ref = models.CharField(_("Reference"),max_length=50,null=True,blank=True)
    salary = models.FloatField(_("Salary"),blank=True,null=True)
    gender = models.CharField(_("Gender"),max_length=50, null=True,blank=True,choices=GENDER_CHOICES)

    schedules = models.ManyToManyField(Schedule,blank=True)

    due_salary = models.FloatField(_("Due Salary"),default=0)

    join_date = models.DateField(_("Joining Date"), null=True,blank=True)

    status =  models.BooleanField(_("Active Status"),default=True)

    def __str__(self) :
        return f'{self.name}'

