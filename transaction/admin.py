from django.contrib import admin
from .models import Credit,Debit, Bill
# Register your models here.
admin.site.register(Credit)
admin.site.register(Debit)
admin.site.register(Bill)