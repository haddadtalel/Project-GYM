from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    context={}
    return render(request, 'home.html',context)




@login_required
def beginners_routines(request):
    return render(request, "beginners_routines.html")

@login_required
def beginner_day1(request):
    return render(request, "beginner_day1.html")

@login_required
def beginner_day2(request):
    return render(request, "beginner_day2.html")

@login_required
def beginner_day3(request):
    return render(request, "beginner_day3.html")

@login_required
def beginner_day4(request):
    return render(request, "beginner_day4.html")

@login_required
def beginner_day5(request):
    return render(request, "beginner_day5.html")

@login_required
def beginner_day6(request):
    return render(request, "beginner_day2.html")

@login_required
def beginner_day7(request):
    return render(request, "beginner_day3.html")

@login_required
def beginner_day8(request):
    return render(request, "beginner_day4.html")

@login_required
def beginner_day9(request):
    return render(request, "beginner_day9.html")

@login_required
def beginner_day10(request):
    return render(request, "beginner_day10.html")

@login_required
def beginner_day11(request):
    return render(request, "beginner_day11.html")
@login_required

def beginner_day12(request):
    return render(request, "beginner_day12.html")

@login_required
def beginner_day13(request):
    return render(request, "beginner_day13.html")

@login_required
def beginner_day14(request):
    return render(request, "beginner_day14.html")

@login_required
def beginner_day15(request):
    return render(request, "beginner_day15.html")

@login_required
def beginner_day16(request):
    return render(request, "beginner_day16.html")

@login_required
def beginner_day17(request):
    return render(request, "beginner_day17.html")

@login_required
def beginner_day18(request):
    return render(request, "beginner_day18.html")

@login_required
def beginner_day19(request):
    return render(request, "beginner_day19.html")

@login_required
def beginner_day20(request):
    return render(request, "beginner_day20.html")

@login_required
def beginner_day21(request):
    return render(request, "beginner_day21.html")

@login_required
def beginner_day22(request):
    return render(request, "beginner_day22.html")
@login_required

def beginner_day23(request):
    return render(request, "beginner_day23.html")
@login_required

def beginner_day24(request):
    return render(request, "beginner_day24.html")

@login_required
def beginner_day25(request):
    return render(request, "beginner_day25.html")

@login_required
def beginner_day26(request):
    return render(request, "beginner_day26.html")

@login_required
def beginner_day27(request):
    return render(request, "beginner_day27.html")
@login_required

def beginner_day28(request):
    return render(request, "beginner_day28.html")

@login_required
def diet_beginner(request):
    return render(request, "diet_beginner.html")

@login_required
def diet_intermediate(request):
    return render(request, "diet_intermediate.html")

@login_required
def diet_hardcore(request):
    return render(request, "diet_hardcore.html")


def services(request):
    return render(request, "services.html")


def gallery(request):
    return render(request, "gallery.html")


def contact(request):
    return render(request, "contact.html")

@login_required
def bmimetric(request):
    return render(request, "Fit.html")
@login_required

def bmistandard(request):
    return render(request, "Standard.html")
