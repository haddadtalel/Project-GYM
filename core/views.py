from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login, logout as lg
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

from django.utils import timezone
from django.db.models import Sum
from datetime import datetime

from user.models import MetaData,User
from member.models import Member
from coach.models import Coach,CoachActivityTrack
from transaction.models import Debit,Credit,Bill
from attendance.models import Attendance

week_day = {
    'Saturday': 0,
    'Sunday': 1,
    'Monday': 2,
    'Tuesday': 3,
    'Wednesday': 4,
    'Thursday': 5,
    'Friday': 6,
}
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
        else:
            messages.error(request,"User not found")
    return render(request,'auth/login.html')

@login_required
def logout(request):
    lg(request)
    return redirect("/")

@login_required
def initialize(request):
    meta = MetaData.objects.last()
    current_month = timezone.now().month
    current_year = timezone.now().year

    lastChecked = str(meta.lastChecked)
    lastChecked = lastChecked[5:7]
    
    if lastChecked != str(current_month):
        # Member
        members = Member.objects.all()
        for member in members:
            if member.package.frequency == "monthly" and member.status == True:
                bill = member.package.price            

                bill_due = bill
                if member.due_payment < 0:
                    bill_due += member.due_payment

                Bill.objects.create(
                    month = datetime.now().strftime("%B"),
                    year= current_year,
                    reason='package_fee',
                    total_amount = bill,
                    payed_amount = 0,
                    due_amount = bill_due,
                    member = member
                ) 

                member.due_payment += bill
                member.save()
        # Coach
        coaches = Coach.objects.all()
        for coach in coaches:
            if coach.status == True:
                salary = coach.salary
                coach.due += salary
                coach.save()
        # Employee
        employees = User.objects.all()
        for employee in employees:
            if employee.is_employee and employee.status == True:
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
    funds = MetaData.objects.last().funds

    # Get the current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Query the income data for the current month
    income_data = Debit.objects.filter(date__month=current_month, date__year=current_year).values('date').annotate(total_amount=Sum('amount')).order_by('date')

    vals_d = {}

    for entry in income_data:
        if entry['date'].strftime('%d') in vals_d:
            vals_d[entry['date'].strftime('%d')] += int(entry['total_amount'])
        else:
            vals_d[entry['date'].strftime('%d')] = int(entry['total_amount'])

    labels_d = list(vals_d.keys())
    data_d = list(vals_d.values())

    expense_data = Credit.objects.filter(date__month=current_month, date__year=current_year).values('date').annotate(total_amount=Sum('amount')).order_by('date')

    vals_c = {}

    for entry in expense_data:
        if entry['date'].strftime('%d') in vals_c:
            vals_c[entry['date'].strftime('%d')] += int(entry['total_amount'])
        else:
            vals_c[entry['date'].strftime('%d')] = int(entry['total_amount'])

    labels_c = list(vals_c.keys())
    data_c = list(vals_c.values())


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
        'current_month_name':current_month_name,
        'funds':funds
    }
    return render(request, "dashboard/manager.html",context)

@login_required
def employeeDashboard(request):
    initialize(request)
    if request.user.is_manager:
        return redirect('/managerDashboard/')
    user = request.user

    current_day = (datetime.now()).strftime('%A')
    current_time = datetime.now().time()

    flag = 0
    schedules = user.get_schedules_filter(current_day)
    for sc in schedules:
        # Within Shift or not
        if sc.start_time <= current_time <= sc.end_time:
            flag = 1
            break

    attendance = Attendance.objects.filter(date__week_day=week_day[current_day],employee = user,attendance = True)
    # Attendance Already Given
    if attendance.count() > 0:
        flag = 2

    # Get Eligible Coach List
    absent_list = []
    if flag != 0:
        coaches = Coach.objects.filter(status = True)
        current_coaches = []
        for coach in coaches:
            schedules = coach.get_schedules_filter(current_day)
            for sc in schedules:
                if sc.start_time <= current_time <= sc.end_time:
                    current_coaches.append(coach)
                    break
        for curr in current_coaches:
            attendances = Attendance.objects.filter(date__week_day=week_day[current_day],coach = curr)
            if attendances.count() == 0:
                absent_list.append(curr)
            else:
                for attendance in attendances:
                    if attendance.attendance == False:
                        absent_list.append(curr)
    context = {
        'user':user,
        'date': datetime.now(),
        'absent_list':absent_list,
        'flag':flag
    }
    return render(request, "dashboard/employee.html",context)

@login_required
def initAttendance(request):
    employees = User.objects.filter(status = True)
    current_day = (datetime.now()).strftime('%A')
    emp_list = []
    for emp in employees:
        schedules = emp.get_schedules_filter(current_day)
        for sc in schedules:
            if sc.day == current_day:
                emp_list.append(emp)

    bulk_employee = []
    for emp in emp_list:
        bulk_employee.append(
            Attendance(
                date = datetime.now(),
                is_employee = True,
                employee = emp,
                attendance = False
            )
        )
    Attendance.objects.bulk_create(bulk_employee)
    # Coach
    coaches = Coach.objects.filter(status = True)
    coach_list = []
    for coach in coaches:
        schedules = coach.get_schedules_filter(current_day)
        for sc in schedules:
            if sc.day == current_day:
                coach_list.append(coach)
    bulk_coach = []
    for coach in coach_list:
        bulk_coach.append(
            Attendance(
                date = datetime.now(),
                is_coach = True,
                coach = coach,
                attendance = False
            )
        )
    Attendance.objects.bulk_create(bulk_coach)

def employeeAttendance(request):
    current_day = (datetime.now()).strftime('%A')

    attendance = Attendance.objects.filter(date__week_day=week_day[current_day])

    if attendance.count() == 0:
        initAttendance(request)
        attendance = Attendance.objects.get(employee = request.user,attendance=False)
        attendance.attendance = True
        attendance.save()
    else:
        attendance = Attendance.objects.get(employee = request.user,attendance=False)
        attendance.attendance = True
        attendance.save()
    return redirect('/employeeDashboard/')

def coachAttendance(request,pk):
    coach = Coach.objects.get(id = pk)
    current_day = (datetime.now()).strftime('%A')

    attendance = Attendance.objects.filter(date__week_day=week_day[current_day])

    if attendance.count() == 0:
        initAttendance(request)
        attendance = Attendance.objects.get(coach = coach,attendance=False)
        attendance.attendance = True
        attendance.save()
    else:
        attendance = Attendance.objects.get(coach = coach,attendance=False)
        attendance.attendance = True
        attendance.save()

    return redirect('/employeeDashboard/')

def coachDashboard(request):
    if request.method == "POST":
        searchCoach = request.POST.get("searchCoach")
        current_datetime = timezone.now()

        try:
            coach = Coach.objects.get(coachId = searchCoach)
            coachActivity = CoachActivityTrack.objects.filter(coach = coach,start_time__gt = current_datetime).order_by("start_time")
            return render(request,"dashboard/coach.html",{'coach':coach,'coachActivity':coachActivity})
        except:
            pass
    return render(request,"dashboard/coach.html")