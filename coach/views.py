from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'coach/index.html')

def edit(request,pk):
    return render(request,"coach/edit.html")