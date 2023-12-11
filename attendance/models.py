from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import User
from coach.models import Coach
# Create your models here.
class Attendance(models.Model):
    date = models.DateTimeField(_("Date"),null=True,blank=True)
    is_coach =  models.BooleanField(_("Is Coach"),default=False)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE,null=True,blank=True)
    is_employee =  models.BooleanField(_("Is Employee"),default=False)
    employee = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    attendance = models.BooleanField(_("Attendance"),default=False)

    def __str__(self) -> str:
        return f'{self.date} | {self.coach} | {self.employee}'