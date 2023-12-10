from django.shortcuts import render,redirect

from .models import Equipment,EquipmentType,EquipmentActivityTrack
from datetime import datetime
# Create your views here.
def index(request):
    eqs = Equipment.objects.all()
    eqTypes = EquipmentType.objects.all()
    eqActivities = EquipmentActivityTrack.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        brand = request.POST.get("brand")
        costCondition = request.POST.get("costCondition")
        serial = request.POST.get("serial")
        price = request.POST.get("price")

        eqTypes_res = request.POST.getlist("eqType")

        print(costCondition)
        print(eqTypes_res)

        if costCondition == "store":
            pass

        eq = Equipment.objects.create(
            name = name,
            brand = brand,
            serial = serial,
            price = price,
            maintenanceDate = datetime.now()
        )
        for eqT in eqTypes_res:
            eq.equipmentType.add(eqT)
        
    context = {
        'eqs':eqs,
        'eqTypes':eqTypes,
        'eqActivities':eqActivities
    }
    return render(request,'equipment/index.html',context)

def edit(request,pk):
    eq = Equipment.objects.get(id = pk)
    eqTypes = EquipmentType.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        brand = request.POST.get("brand")
        eqTypes_res = request.POST.getlist("eqType")

        eq.name = name
        eq.brand = brand

            
        eq.save()

        eq.equipmentType.clear()
        for eqT in eqTypes_res:
            eq.equipmentType.add(eqT)

    context = {
        'eq':eq,
        'eqTypes':eqTypes
    }
    return render(request,"equipment/edit.html",context)

def book(request):
    return render(request,"equipment/book.html")

def deactivate(request,pk):
    eq = Equipment.objects.get(id = pk)
    eq.is_available = False
    eq.save()
    return redirect("/equipment/")

def active(request,pk):
    eq = Equipment.objects.get(id = pk)
    eq.is_available = True
    eq.save()
    return redirect("/equipment/")

def delete(request,pk):
    Equipment.objects.get(id = pk).delete()
    return redirect("/equipment/")