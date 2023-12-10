from django.shortcuts import render,redirect

from .models import Package, FREQUENCY_CHOICES
from schedule.models import Schedule
from equipment.models import EquipmentType
# Create your views here.
def index(request):
    packages = Package.objects.all().order_by("-id")
    schedules = Schedule.objects.filter(name="package")
    eqTypes = EquipmentType.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        desc = request.POST.get("desc")
        freq = request.POST.get("paymentFreq")
        schedules_res = request.POST.getlist("schedules")
        eqTypes_res = request.POST.getlist("eqType")

        package = Package.objects.create(
            name = name,
            price = price,
            desc = desc,
            frequency = freq
        )

        for schedule in schedules_res:
            package.schedules.add(schedule)

        for eq in eqTypes_res:
            package.equipmentType.add(eq)

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

    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        desc = request.POST.get("desc")
        freq = request.POST.get("paymentFreq")
        schedules_res = request.POST.getlist("schedule")
        eqTypes_res = request.POST.getlist("eqType")

        package.name = name
        package.price = price
        package.desc = desc
        package.frequency = freq

        package.schedules.clear()
        for schedule in schedules_res:
            package.schedules.add(schedule)
        package.equipmentType.clear()
        for eq in eqTypes_res:
            package.equipmentType.add(eq)
    context = {
        'package':package,
        'schedules':schedules,
        'eqTypes':eqTypes,
        'FREQUENCY_CHOICES':FREQUENCY_CHOICES
    }
    return render(request,"package/edit.html",context)

def delete(request,pk):
    Package.objects.get(id = pk).delete()
    return redirect("/package/")