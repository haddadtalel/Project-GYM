from django.shortcuts import render,redirect

from .models import Schedule,TYPE_CHOICE,DAY_CHOICES
# Create your views here.
def index(request):
    schedules = Schedule.objects.all().order_by("-id")

    if request.method == "POST":
        name = request.POST.get("name")
        day = request.POST.get("day")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        Schedule.objects.create(
            name = name,
            day = day,
            start_time = start_time,
            end_time = end_time
        )

    context = {
        'schedules':schedules,
        'DAY_CHOICES':DAY_CHOICES,
        'TYPE_CHOICE':TYPE_CHOICE
    }
    return render(request,'schedule/index.html',context)

def edit(request,pk):
    schedule = Schedule.objects.get(id = pk)

    print(schedule)

    if request.method == "POST":
        name = request.POST.get("name")
        day = request.POST.get("day")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        schedule.name = name
        schedule.day = day
        if start_time != "":
            schedule.start_time = start_time
        if end_time != "":
            schedule.end_time = end_time

        schedule.save()
        return redirect("/schedule/")
    context = {
        'schedule':schedule,
        'DAY_CHOICES':DAY_CHOICES,
        'TYPE_CHOICE':TYPE_CHOICE
    }

    return render(request,"schedule/edit.html",context)

def delete(request,pk):
    Schedule.objects.get(id = pk).delete()
    return redirect("/schedule/")