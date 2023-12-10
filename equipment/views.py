from django.shortcuts import render,redirect
from datetime import datetime

from .models import Equipment,EquipmentType,EquipmentActivityTrack
from user.models import MetaData
from transaction.models import Credit
# Create your views here.
def index(request):
    eqs = Equipment.objects.all()
    eqTypes = EquipmentType.objects.all()
    eqActivities = EquipmentActivityTrack.objects.all()

    meta = MetaData.objects.last()
    if request.method == "POST":
        name = request.POST.get("name")
        brand = request.POST.get("brand")
        costCondition = request.POST.get("costCondition")
        serial = request.POST.get("serial")
        price = request.POST.get("price")

        eqTypes_res = request.POST.getlist("eqType")


        eq = Equipment.objects.create(
            name = name,
            brand = brand,
            serial = serial,
            price = price,
            maintenanceDate = datetime.now()
        )
        for eqT in eqTypes_res:
            eq.equipmentType.add(eqT)
        
        timestamp = int(datetime.now().timestamp())
        if costCondition == "store":
            Credit.objects.create(
                trxId = 'FK-TRX-' + str(timestamp),
                reason = 'buy_equipment',
                amount = int(price),
                date = datetime.now(),
                is_equipment = True,
                equipment = eq
            )
            meta.funds -= int(price)
            meta.save()
        
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
    eq.maintenanceDate = datetime.now()
    eq.save()
    return redirect("/equipment/")

def delete(request,pk):
    Equipment.objects.get(id = pk).delete()
    return redirect("/equipment/")