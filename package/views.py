from django.shortcuts import render

from .models import Package, FREQUENCY_CHOICES
from schedule.models import Schedule
from equipment.models import EquipmentType
# Create your views here.
def index(request):
    packages = Package.objects.all()
    schedules = Schedule.objects.filter(name="package")
    eqTypes = EquipmentType.objects.all()

    context = {
        'packages':packages,
        'schedules':schedules,
        'eqTypes':eqTypes,
        'FREQUENCY_CHOICES':FREQUENCY_CHOICES
    }
    return render(request,'package/index.html',context)

def edit(request,pk):
    package = Package.objects.get(id = pk)
    schedules = Schedule.objects.filter(name="package")
    eqTypes = EquipmentType.objects.all()

    context = {
        'package':package,
        'schedules':schedules,
        'eqTypes':eqTypes,
        'FREQUENCY_CHOICES':FREQUENCY_CHOICES
    }
    return render(request,"package/edit.html",context)