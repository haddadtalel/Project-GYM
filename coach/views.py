from django.shortcuts import render,redirect

from schedule.models import Schedule
from .models import Coach
# Create your views here.
def index(request):
    schedules = Schedule.objects.filter(name = 'coach')
    coaches = Coach.objects.all().order_by("-id")

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        dob = request.POST.get("dob")
        nid = request.POST.get("nid")
        gender = request.POST.get("gender")
        salary = request.POST.get("salary")
        address = request.POST.get("address")
        ref = request.POST.get("red")
        schedules_res = request.POST.getlist("schedule")

        lastId = Coach.objects.last().id

        coach = Coach.objects.create(
            name = name,
            phone = phone,
            dob = dob,
            nid = nid,
            gender = gender,
            salary = salary,
            address = address,
            ref = ref,
            coachId = "FKC-" + str(lastId+1)
        )

        for schedule in schedules_res:
            coach.schedules.add(schedule)
    context = {
        'schedules':schedules,
        'coaches':coaches
    }

    return render(request,'coach/index.html',context)

def edit(request,pk):
    coach = Coach.objects.get(id = pk)
    schedules = Schedule.objects.filter(name = 'coach')

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        nid = request.POST.get("nid")
        salary = request.POST.get("salary")
        address = request.POST.get("address")
        ref = request.POST.get("ref")
        schedules_res = request.POST.getlist("schedule")

        coach.name = name
        coach.phone = phone
        coach.salary = salary
        coach.nid = nid
        coach.address = address
        coach.ref = ref
            
        coach.save()

        coach.schedules.clear()
        for schedule in schedules_res:
            coach.schedules.add(schedule)


    context = {
        'coach': coach,
        'schedules':schedules
    }
    return render(request,"coach/edit.html",context)

def book(request):
    return render(request,"coach/book.html")

def deactivate(request,pk):
    coach = Coach.objects.get(id = pk)
    coach.status = False
    coach.save()
    return redirect("/coach/")

def active(request,pk):
    employee = Coach.objects.get(id = pk)
    employee.status = True
    employee.save()
    return redirect("/coach/")

def delete(request,pk):
    Coach.objects.get(id = pk).delete()
    return redirect("/coach/")