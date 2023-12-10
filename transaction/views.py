from django.shortcuts import render, redirect
from django.db.models import Q
from datetime import datetime

from .models import Credit,Debit
from user.models import User
from coach.models import Coach
from user.models import MetaData


# Create your views here.
def index(request):
    debits = Debit.objects.all().order_by("-date")
    credits = Credit.objects.all().order_by("-date")

    employees = User.objects.filter(due__gt = 0)
    coaches = Coach.objects.filter(due__gt = 0)

    if request.method == "POST":
        searchCoach = request.POST.get("searchCoach")
        searchEmp = request.POST.get("searchEmp")

        if searchCoach != "":
            coaches = Coach.objects.filter(Q(name__icontains=searchCoach) | Q(coachId__icontains=searchCoach))

        if searchEmp != "":
            employees = User.objects.filter(Q(name__icontains=searchEmp) | Q(emp_id__icontains=searchEmp))

    context = {
        'debits':debits,
        'credits':credits,
        'employees':employees,
        'coaches':coaches,
    }
    return render(request,'transaction/index.html',context)


def payE(request,pk):
    employee = User.objects.get(id = pk)
    
    if request.method == "POST":
        amount = request.POST.get("amount")

        timestamp = int(datetime.now().timestamp())
        employee.due -= int(amount)

        employee.save()

        Credit.objects.create(
            trxId = 'FK-TRX-' + str(timestamp),
            reason = 'salary_employee',
            amount = int(amount),
            date = datetime.now(),
            is_employee = True,
            employee = employee
        )
        meta = MetaData.objects.last()
        meta.funds -= int(amount)
        meta.save()

        return redirect("/transaction/")
    context = {
        'employee':employee
    }
    return render(request,'transaction/payEmployee.html',context)

def payC(request,pk):
    coach = Coach.objects.get(id = pk)
    
    if request.method == "POST":
        amount = request.POST.get("amount")

        timestamp = int(datetime.now().timestamp())
        coach.due -= int(amount)

        coach.save()

        Credit.objects.create(
            trxId = 'FK-TRX-' + str(timestamp),
            reason = 'salary_coach',
            amount = int(amount),
            date = datetime.now(),
            is_coach = True,
            coach = coach
        )
        meta = MetaData.objects.last()
        meta.funds -= int(amount)
        meta.save()
        
        return redirect("/transaction/")
    context = {
        'coach':coach
    }
    return render(request,'transaction/payCoach.html',context)