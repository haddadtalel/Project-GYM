from django.contrib import admin
from .models import Equipment, EquipmentActivityTrack, EquipmentType
# Register your models here.
admin.site.register(EquipmentType)
admin.site.register(Equipment)
admin.site.register(EquipmentActivityTrack)