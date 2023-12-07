from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from schedule.models import Schedule

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
]

# Create your models here.
class User(AbstractUser):
    phone = models.CharField(_("Phone"),unique=True,max_length=11,blank=True,null=True)
    name = models.CharField(_("Full Name"),max_length=50,null=True,blank=True)
    dob = models.DateField(_("Date of Birth"),null=True,blank=True)
    
    is_manager = models.BooleanField(_("Manager"),default=False)
    is_employee = models.BooleanField(_("Employee"),default=True)
    
    salary = models.FloatField(_("Salary"),blank=True,null=True)
    gender = models.CharField(_("Gender"),max_length=50, null=True,blank=True,choices=GENDER_CHOICES)

    schedules = models.ManyToManyField(Schedule,blank=True)

    due_payment = models.FloatField(_("Due Payment"),default=0)
    
    join_date = models.DateField(_("Joining Date"), null=True,blank=True)

    status =  models.BooleanField(_("Active Status"),default=True)

    def __str__(self) :
        return f'{self.username}'

