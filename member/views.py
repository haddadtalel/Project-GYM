from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'member/index.html')

def edit(request,pk):
    return render(request,"member/edit.html")

def bill(request):
    return render(request,"member/bill.html")