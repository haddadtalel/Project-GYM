from django.db import models
from django.utils.translation import gettext_lazy as _
from package.models import Package

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
]

# Create your models here.
class Member(models.Model):
    memberId = models.CharField(_("Member Id"),max_length=20,null=True,blank=True)
    name = models.CharField(_("Full Name"),max_length=50,null=True,blank=True)
    phone = models.CharField(_("Phone"),unique=True,max_length=11,blank=True,null=True)
    dob = models.DateField(_("Date of Birth"),null=True,blank=True)
    
    ref = models.CharField(_("Reference"),unique=True,max_length=50,blank=True,null=True)
    address = models.TextField(_("Address"),null=True,blank=True)
    gender = models.CharField(_("Gender"),max_length=50, null=True,blank=True,choices=GENDER_CHOICES)

    package = models.ForeignKey(Package,on_delete=models.CASCADE,null=True,blank=True)

    due_payment = models.FloatField(_("Due Payment"),default=0)

    join_date = models.DateField(_("Joining Date"), null=True,blank=True)
    status =  models.BooleanField(_("Active Status"),default=True)


    def __str__(self) :
        return f'{self.name} - {self.dob}'

