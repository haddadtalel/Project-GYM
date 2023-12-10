from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.hashers import make_password

from user.models import User
from schedule.models import Schedule

# Create your views here.
def index(request):
    employees = User.objects.filter(is_employee = True)
    schedules = Schedule.objects.filter(name = 'stuff')

    if request.method == "POST":
        username = request.POST.get("username")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        dob = request.POST.get("dob")
        nid = request.POST.get("nid")
        gender = request.POST.get("gender")
        salary = request.POST.get("salary")
        address = request.POST.get("address")
        password = request.POST.get("password")
        schedules_res = request.POST.getlist("schedule")

        lastId = User.objects.last().id

        user = User.objects.create(
            username = username,
            name = name,
            phone = phone,
            dob = dob,
            nid = nid,
            gender = gender,
            salary = salary,
            address = address,
            password = make_password(password),
            emp_id = "FKE-" + str(lastId+1)
        )

        for schedule in schedules_res:
            user.schedules.add(schedule)

    context = {
        'employees':employees,
        'schedules':schedules
    }
    return render(request,'user/index.html',context)

def edit(request,pk):
    employee = User.objects.get(id = pk)
    schedules = Schedule.objects.filter(name = 'stuff')

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        nid = request.POST.get("nid")
        salary = request.POST.get("salary")
        address = request.POST.get("address")
        password = request.POST.get("password")
        schedules_res = request.POST.getlist("schedule")

        employee.name = name
        employee.phone = phone
        employee.salary = salary
        employee.nid = nid
        employee.address = address

        if password != "":
            employee.password = make_password(password)
            
        employee.save()

        employee.schedules.clear()
        for schedule in schedules_res:
            employee.schedules.add(schedule)

    context = {
        'employee': employee,
        'schedules':schedules
    }
    return render(request,"user/edit.html",context)

def deactivate(request,pk):
    employee = User.objects.get(id = pk)
    employee.is_active = False
    employee.save()
    return redirect("/user/")

def active(request,pk):
    employee = User.objects.get(id = pk)
    employee.is_active = True
    employee.save()
    return redirect("/user/")

def delete(request,pk):
    User.objects.get(id = pk).delete()
    return redirect("/user/")