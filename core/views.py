from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login, logout as lg
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    # Redirect the user if he is authenticated
    if request.user.is_authenticated:
        return redirect('/member/')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            next_url = request.GET.get('next')
            if next_url:
                success_url = next_url
            else:
                success_url = "/coach/"
            login(request,user)   
            # Redirect the user to suitable url
            return redirect(success_url)
    return render(request,'auth/login.html')

@login_required
def logout(request):
    lg(request)
    return redirect("/")

def managerDashboard(request):
    return render(request, "dashboard/manager.html")