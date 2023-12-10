from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login, logout as lg
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from django.db.models import Sum
from datetime import datetime

from user.models import MetaData,User
from member.models import Member
from coach.models import Coach
from transaction.models import Debit,Credit
# Create your views here.

def index(request):
    # Redirect the user if he is authenticated
    if request.user.is_authenticated:
        if request.user.is_manager:
            return redirect('/managerDashboard/')
        else:
            return redirect('/employeeDashboard/')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            next_url = request.GET.get('next')
            if next_url:
                success_url = next_url
            else:
                success_url = "/employeeDashboard/"
            login(request,user)   
            # Redirect the user to suitable url
            return redirect(success_url)
    return render(request,'auth/login.html')

@login_required
def logout(request):
    lg(request)
    return redirect("/")

@login_required
def initialize(request):
    meta = MetaData.objects.last()
    current_month = timezone.now().month

    lastChecked = str(meta.lastChecked)
    lastChecked = lastChecked[5:7]
    
    if lastChecked != str(current_month):
        # Member
        members = Member.objects.all()
        for member in members:
            bill = 0
            if member.package.frequency == "monthly":
                bill = member.package.price
            member.due_payment += bill
            member.save()
        # Coach
        coaches = Coach.objects.all()
        for coach in coaches:
            salary = coach.salary
            coach.due += salary
            coach.save()
        # Employee
        employees = User.objects.all()
        for employee in employees:
            if employee.is_employee:
                salary = employee.salary
                employee.due += salary
                employee.save()

    meta.lastChecked = timezone.now()
    meta.save()

@login_required
def managerDashboard(request):
    initialize(request)
    current_month_name = timezone.now().strftime('%B')

    coaches_count = Coach.objects.all().count
    members_count = Member.objects.all().count
    employees_count = User.objects.filter(is_employee = True).count

    coaches = Coach.objects.filter(due__gt = 0)
    employees = User.objects.filter(due__gt = 0,is_employee = True)
    members = Member.objects.all().order_by("-id")


    # Get the current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Query the income data for the current month
    income_data = Debit.objects.filter(date__month=current_month, date__year=current_year).values('date').annotate(total_amount=Sum('amount')).order_by('date')

    # Query the income data for the current month

    # Prepare the data for the chart
    labels_d = [entry['date'].strftime('%d') for entry in income_data]
    data_d = [entry['total_amount'] for entry in income_data]

    expense_data = Credit.objects.filter(date__month=current_month, date__year=current_year).values('date').annotate(total_amount=Sum('amount')).order_by('date')

    labels_c = [entry['date'].strftime('%d') for entry in expense_data]
    data_c = [entry['total_amount'] for entry in expense_data]

    context = {
        'coaches':coaches,
        'coaches_count':coaches_count,
        'members_count':members_count,
        'employees_count':employees_count,
        'employees':employees,
        'members':members,
        'labels_d': labels_d,
        'data_d': data_d,
        'labels_c': labels_c,
        'data_c': data_c,
        'current_month_name':current_month_name
    }
    return render(request, "dashboard/manager.html",context)

@login_required
def employeeDashboard(request):
    if request.user.is_manager:
        return redirect('/managerDashboard/')
    return render(request, "dashboard/employee.html")

def coachDashboard(request):
    return render(request,"dashboard/coach.html")