from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from datetime import datetime

from .models import Member
from package.models import Package
from transaction.models import Debit
from user.models import MetaData
# Create your views here.
def index(request):
    members = Member.objects.all().order_by("-due_payment")
    packages = Package.objects.all().order_by("-id")

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        dob = request.POST.get("dob")
        nid = request.POST.get("nid")
        gender = request.POST.get("gender")
        packageId = request.POST.get("package")
        address = request.POST.get("address")
        ref = request.POST.get("ref")

        lastId = Member.objects.last().id

        Member.objects.create(
            name = name,
            phone = phone,
            dob = dob,
            nid = nid,
            gender = gender,
            package = Package.objects.get(id = packageId),
            address = address,
            ref = ref,
            due_payment = Package.objects.get(id = packageId).price,
            memberId = "FKM-" + str(lastId+1)
        )
    context = {
        'members':members,
        'packages':packages
    }
    return render(request,'member/index.html',context)

def edit(request,pk):
    member = Member.objects.get(id = pk)
    packages = Package.objects.all().order_by("-id")

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        nid = request.POST.get("nid")
        packageId = request.POST.get("package")
        address = request.POST.get("address")
        ref = request.POST.get("ref")

        member.name = name
        member.phone = phone
        member.nid = nid
        member.ref = ref
        if member.package.id != int(packageId):
            member.package = Package.objects.get(id=packageId)
            member.due_payment += Package.objects.get(id=packageId).price
        member.address = address

        member.save()
        
    context = {
        'member':member,
        'packages':packages
    }
    return render(request,"member/edit.html",context)

def bill(request):
    members = Member.objects.filter(due_payment__gt =0).order_by("-due_payment")

    if request.method == "POST":
        search = request.POST.get("search")
        members = Member.objects.filter(Q(name__icontains=search) | Q(memberId__icontains=search))

    context = {
        'members':members,
    }
    return render(request,"member/bill.html",context)

def pay(request):
    if request.method == "POST":
        memberId = request.POST.get("memberId")
        amount = request.POST.get("amount")

        try:
            timestamp = int(datetime.now().timestamp())
            meta = MetaData.objects.last()

            member = Member.objects.get(memberId = memberId)
            if member.status == False:
                messages.error(request,"Member Profile is deactivated")
                return redirect("/member/bill/")
            
            member.due_payment -= int(amount)

            Debit.objects.create(
                trxId = "FK-TRX-" + str(timestamp),
                reason = "package",
                amount = int(amount),
                date = datetime.now(),
                payed_by = member,
                received_by = request.user
            )
            meta.funds += int(amount)
            meta.save()
            member.save()
        except:
            messages.error(request,"Wrong Member Id")
    return redirect("/member/bill/")

def deactivate(request,pk):
    member = Member.objects.get(id = pk)
    member.status = False
    member.save()
    return redirect("/member/")

def active(request,pk):
    member = Member.objects.get(id = pk)
    member.status = True
    member.save()
    return redirect("/member/")

def delete(request,pk):
    Member.objects.get(id = pk).delete()
    return redirect("/member/")