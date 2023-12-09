from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'user/index.html')

def edit(request,pk):
    return render(request,"user/edit.html")