from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q, Sum
from django.contrib import messages
from datetime import datetime
import datetime as dt

from .models import Member
from package.models import Package
from transaction.models import Debit, Bill
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

        packageId = packageId.split(" ");
        packageId = packageId[0]
        address = request.POST.get("address")
        ref = request.POST.get("ref")
        amount = request.POST.get("amount")
        due = request.POST.get("due_amount")

        try:
            lastId = Member.objects.last().id
        except:
            lastId = 0

        package = Package.objects.get(id = packageId)
        # Get Current Month Name
        month = datetime.now().strftime("%B")
        # Get the current year
        year = datetime.now().year

        if int(amount) > package.price:
            memberDue = package.price - int(amount)
        else:
            memberDue = int(due) 

        member = Member.objects.create(
            name = name,
            phone = phone,
            dob = dob,
            nid = nid,
            gender = gender,
            package = Package.objects.get(id = packageId),
            address = address,
            ref = ref,
            due_payment = int(memberDue),
            memberId = "FKM-" + str(lastId+1),
            join_date = datetime.now()
        )

        Bill.objects.create(
            month = month,
            year=year,
            reason='package_admission',
            total_amount = package.price,
            payed_amount = amount,
            due_amount = due,
            member = member
        ) 

        timestamp = int(datetime.now().timestamp())
        meta = MetaData.objects.last()

        Debit.objects.create(
            trxId = "FK-TRX-" + str(timestamp),
            reason = "admission",
            amount = int(amount),
            date = datetime.now(),
            payed_by = member,
            received_by = request.user
        )
        meta.funds += int(amount)
        meta.save()

    context = {
        'members':members,
        'packages':packages
    }
    return render(request,'member/index.html',context)

def edit(request,pk):
    member = Member.objects.get(id = pk)
    packages = Package.objects.all().order_by("-id")
    bills = Bill.objects.filter(member = member).order_by("-id")
    month = datetime.now().strftime("%B")
    
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
        'packages':packages,
        'bills':bills,
        'month':month
    }
    return render(request,"member/edit.html",context)

def bill(request):
    members = Member.objects.filter(due_payment__gt =0,status=True).order_by("-due_payment")

    if request.method == "POST":
        search = request.POST.get("search")
        members = Member.objects.filter(Q(name__icontains=search) | Q(memberId__icontains=search))

    context = {
        'members':members,
    }
    return render(request,"member/bill.html",context)

def getPreviousMonth(request):
    # Get the current date and time
    current_date = datetime.now()

    # Calculate the previous month
    previous_month = current_date.replace(day=1) - dt.timedelta(days=1)

    # Get the previous month's name
    previous_month_name = previous_month.strftime("%B")

    # Print the previous month's name
    return previous_month_name

def pay(request):
    # Get Current Month Name
    month = datetime.now().strftime("%B")
    # Get the current year
    year = datetime.now().year

    if request.method == "POST":
        memberId = request.POST.get("memberId")
        amount = request.POST.get("amount")

        total_amount = amount
        try:
            timestamp = int(datetime.now().timestamp())
            meta = MetaData.objects.last()

            member = Member.objects.get(memberId = memberId)
            if member.status == False:
                messages.error(request,"Member Profile is deactivated")
                return redirect("/member/bill/")
            
            member.due_payment -= int(amount)

            flag = True

            try:
                prev_month = getPreviousMonth(request)
                prev_bill = Bill.objects.get(member = member, month = prev_month,due_amount__gt = 0)
            except:
                flag = False

            updateThisMonth = True

            if flag:
                left_amount = float(amount) - prev_bill.due_amount
                
                if left_amount <= 0:
                    prev_bill.due_amount -= float(amount)
                    updateThisMonth = False
                else:
                    amount = left_amount
                    prev_bill.due_amount = 0

                prev_bill.save()


            if updateThisMonth:
                bill = Bill.objects.get(member = member, month = month)
                if amount > bill.due_amount:
                    bill.advanced_amount = float(amount - bill.due_amount)
                    bill.due_amount = 0
                else:
                    bill.due_amount -= amount

                bill.payed_amount = float(total_amount)

                bill.save()
                

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