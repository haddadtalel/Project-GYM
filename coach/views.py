from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib import messages
from datetime import datetime, timedelta

from schedule.models import Schedule
from .models import Coach, CoachActivityTrack
from member.models import Member
from transaction.models import Debit
from user.models import MetaData
from attendance.models import Attendance
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

    current_month = datetime.now().month
    current_year = datetime.now().year

    # Query the income data for the current month
    attendance = Attendance.objects.filter(date__month=current_month, date__year=current_year,coach=coach)
    
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
        'schedules':schedules,
        'attendance':attendance
    }
    return render(request,"coach/edit.html",context)

def activity(request):
    coaches = Coach.objects.all().order_by("-id")
    members = Member.objects.all()
    coachActivities = CoachActivityTrack.objects.all().order_by("start_time")
    if request.method == "POST":
        search = request.POST.get("searchCoach")
        coaches = Coach.objects.filter(Q(name__icontains=search) | Q(coachId__icontains=search))

    context = {
        'coaches': coaches,
        'coachActivities':coachActivities,
        'members':members
    }
    return render(request,"coach/book.html",context)

def book(request):
    if request.method == "POST":
        coachId = request.POST.get("coachId")
        memId = request.POST.get("memId")
        date = request.POST.get("date")
        amount = request.POST.get("amount")

        timestamp = int(datetime.now().timestamp())
        start_time = datetime.strptime(date, '%Y-%m-%dT%H:%M')
        end_time = start_time + timedelta(hours=2)

        selectedStartTime = start_time.time()
        selectedEndTime = end_time.time()
        # For Coach
        try:
            coach = Coach.objects.get(coachId = coachId)
        except:
            messages.error(request,"Wrong Coach Id")    
            return redirect("/coach/activity/")

        check_start_time = False
        check_end_time = False        
        schedules = coach.get_schedules_filter(start_time.strftime('%A'))

        if schedules.count() == 0:
            messages.error(request,"Selected Coach has no schedule on selected date")    
            return redirect("/coach/activity/")          
          
        for sc in schedules:
            if sc.start_time <= selectedStartTime <= sc.end_time:
                check_start_time = True

            if sc.start_time <= selectedEndTime <= sc.end_time:
                check_end_time = True

        if check_start_time == False or check_end_time == False:
            messages.error(request,"Coach is not available at selected time")
            return redirect("/coach/activity/")       

        # For member
        current_day = (datetime.now()).strftime('%A')

        try:
            # Check for member session fee
            member = Member.objects.get(memberId = memId)
            if member.status == False:
                messages.error(request,"Member Account Deactivated")      
            else:
                premium = False
                for eqT in member.package.get_equipmentTypes():
                    if eqT.name == "Premium":
                        premium = True           
            if premium:
                if int(amount) != 200:
                    messages.error(request,"Premium Member Session Fee 200 Taka") 
                    return redirect("/coach/activity/")   
            else:  
                if int(amount) != 400:
                    messages.error(request,"Basic Member Session Fee 400 Taka") 
                    return redirect("/coach/activity/")             
            # Check for member schedule
            check_start_time = False
            check_end_time = False        
            schedules = member.package.get_schedules_filter(current_day)
            for sc in schedules:
                if sc.start_time <= selectedStartTime <= sc.end_time:
                    check_start_time = True

                if sc.start_time <= selectedEndTime <= sc.end_time:
                    check_end_time = True
            if check_start_time == False or check_end_time == False:
                messages.error(request,"Member Package Does not support selected time")
                return redirect("/coach/activity/")
            
            # Member and Coach ok   
            coachActivity = CoachActivityTrack.objects.filter(Q(start_time__range=(start_time,end_time)) | Q(end_time__range=(start_time,end_time)),coach = coach).count()

            if coachActivity != 0:
                messages.error(request,"Schedule Already Booked")
            else:
                CoachActivityTrack.objects.create(
                    start_time = start_time,
                    end_time = end_time,
                    booked_by= request.user,
                    booked_for = member,
                    coach = coach
                )    
                Debit.objects.create(
                    trxId = "FK-TRX-" + str(timestamp),
                    reason = 'private_session',
                    amount = int(amount),
                    date = datetime.now(),
                    payed_by = member,
                    received_by = request.user
                )
                meta = MetaData.objects.last()
                meta.funds += int(amount)
                meta.save()
        except:
            messages.error(request,"Wrong Member Id")    


        # start_time = datetime.strptime(date, '%Y-%m-%dT%H:%M')
        # end_time = start_time + timedelta(hours=1)

        # # For member
        # current_day = (datetime.now()).strftime('%A')

        # selectedStartTime = start_time.time()
        # selectedEndTime = end_time.time()
        # try:
        #     eq = Equipment.objects.get(serial = serial)
        #     try:
        #         member = Member.objects.get(memberId=memId)
        #         if member.status == False:
        #             messages.error(request,"Member Account Deactivated")      
        #         else:
        #             # Check if member package supports selected time
        #             check_start_time = False
        #             check_end_time = False        
        #             schedules = member.package.get_schedules_filter(current_day)
        #             for sc in schedules:
        #                 if sc.start_time <= selectedStartTime <= sc.end_time:
        #                     check_start_time = True

        #                 if sc.start_time <= selectedEndTime <= sc.end_time:
        #                     check_end_time = True
        #             if check_start_time == False or check_end_time == False:
        #                 messages.error(request,"Member Package Does not support selected time")
        #                 return redirect("/equipment/activity/")
        #             # Check if member package supports selected equipment   
        #             flag = False                
        #             for eqT in eq.get_eqTypes():
        #                 for packageEqT in member.package.get_equipmentTypes():
        #                     if eqT.id == packageEqT.id:
        #                         flag = True
        #             # Equipment and Member Correct  
        #             if flag:
        #                 eqActivityCount = EquipmentActivityTrack.objects.filter(Q(start_time__range=(start_time,end_time)) | Q(end_time__range=(start_time,end_time)),equipment = eq,is_active = True).count()
        #                 if eqActivityCount != 0:
        #                     messages.error(request,"Schedule Already Booked")
        #                 else:
        #                     EquipmentActivityTrack.objects.create(
        #                         start_time = start_time,
        #                         end_time = end_time,
        #                         booked_by= request.user,
        #                         booked_for = member,
        #                         equipment = eq
        #                     )    
        #             else:
        #                 messages.error(request,"Member Package Doesn't Support Selected Equipment")           
        #     except:
        #         messages.error(request,"Wrong Member Id")    
        # except:
        #     messages.error(request,"Wrong Equipment Serial")    
    return redirect("/coach/activity/")

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