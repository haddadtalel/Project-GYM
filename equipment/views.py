from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'equipment/index.html')

def edit(request,pk):
    return render(request,"equipment/edit.html")

def book(request):
    return render(request,"equipment/book.html")