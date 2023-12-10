from django.db import models
from django.utils.translation import gettext_lazy as _
from member.models import Member
from user.models import User
from coach.models import Coach
from equipment.models import Equipment

DEBIT_REASONS = [
    ('package', 'Package'),
    ('private_session', 'Private Session'),
]

CREDIT_REASONS = [
    ('salary_coach', 'Coach Salary'),
    ('salary_employee', 'Employee Salary'),
    ('buy_equipment', 'Buy Equipment'),
]

# Create your models here.
# Incoming
class Debit(models.Model):
    trxId = models.CharField(_("Transaction Id"),max_length=20,null=True,blank=True)

    reason = models.CharField(_("Reason"),max_length=50, null=True,blank=True,choices=DEBIT_REASONS)

    amount = models.FloatField(_("Amount"),null=True,blank=True)
    date = models.DateTimeField(_("Date"), null=True,blank=True)
    payed_by = models.ForeignKey(Member, on_delete=models.CASCADE,null=True,blank=True)
    received_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self) :
        return f'{self.trxId} - {self.amount}'
    
# Outgoing
class Credit(models.Model):
    trxId = models.CharField(_("Transaction Id"),max_length=20,null=True,blank=True)

    reason = models.CharField(_("Reason"),max_length=50, null=True,blank=True,choices=CREDIT_REASONS)

    amount = models.FloatField(_("Amount"),null=True,blank=True)
    date = models.DateTimeField(_("Date"), null=True,blank=True)
    is_employee = models.BooleanField(_("Is Employee"),default=False)
    employee = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    is_coach= models.BooleanField(_("Is Coach"),default=False)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE,null=True,blank=True)
    is_equipment= models.BooleanField(_("Is Equipment"),default=False)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self) :
        return f'{self.trxId} - {self.amount}'

