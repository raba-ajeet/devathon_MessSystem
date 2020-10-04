from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib.auth import login,logout,authenticate
# Create your views here.
def home(request):    
    return render(request,'mess/home.html')


def signupuser(request):
    if request.method=='GET':
        return render(request,'mess/signup1.html')
    else:
        try:
            user=User.objects.create_user(request.POST['username'],password=request.POST['password'])
            user.save()
            login(request,user)
            if request.POST.get('messstaff',None)=='1':
                if request.POST['registration_num']=='2020':
                    messstaff=MessStaff(username=request.POST['username'],password=request.POST['password'],unique_code=request.POST['registration_num'])
                    messstaff.save()
                else:
                    print(request.POST['registration_num'])
                    return render(request,'mess/signup1.html',{'warning':"fill the correct code or username"})
            else :
                messuser=MessUser(username=request.POST['username'],password=request.POST['password'],registration_no=request.POST['registration_num'])
                messuser.save()
            return redirect(home)
        except IntegrityError:
            return render(request,'mess/signup1.html',{'warning':"username is already taken"})
            # return render(request,'todo/home.html')

def loginuser(request):
    if request.method=='POST':
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'mess/login.html',{'warning':"username and password didn't match"})
        else:
            login(request,user)
            checkuser=MessStaff.objects.filter(username=request.POST['username'])
            if checkuser is None:
                # I m Mess user
                print("I m MessUser")
                return redirect(home)
            else:
                # I m Mess Staff 
                print("I m MessStaff")
                return redirect(home)
    else:
        return render(request,'mess/login.html')

def logoutuser(request):
    if request.method=='POST':
        logout(request)
        return redirect('home')


def itemslist(request):
    items=Item.objects.all()
    return render(request,'mess/items.html',{'items':items})

def view_orders(request):
    # orders=Booking.objects.all()
    orders=Booking.objects.all().annotate(total=Sum('item_booked__price'))
    return render(request,'mess/messuserhome.html',{'orders':orders})