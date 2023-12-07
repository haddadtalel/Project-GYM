from django.db import models
from django.utils.translation import gettext_lazy as _
from member.models import Member
from user.models import User

TRANSACTION_REASONS = [
    ('package', 'Package'),
    ('private_session', 'Private Session'),
    ('salary_coach', 'Coach Salary'),
    ('salary_employee', 'Employee Salary'),
]

TRANSACTION_TYPES = [
    ('credit', 'Credit'),
    ('debit', 'Debit'),
]

# Create your models here.
class Transaction(models.Model):
    trxId = models.CharField(_("Transaction Id"),max_length=20,null=True,blank=True)

    reason = models.CharField(_("Reason"),max_length=50, null=True,blank=True,choices=TRANSACTION_REASONS)

    transactionType = models.CharField(_("Transaction Type"),max_length=50, null=True,blank=True,choices=TRANSACTION_TYPES)

    amount = models.FloatField(_("Amount"),null=True,blank=True)
    date = models.DateTimeField(_("Date"), null=True,blank=True)
    payed_by = models.ForeignKey(Member, on_delete=models.CASCADE,null=True,blank=True)
    received_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self) :
        return f'{self.trxId}'

