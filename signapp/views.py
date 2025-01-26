from django.shortcuts import render,redirect,get_object_or_404
from .forms import user_reg,user_log
from django.contrib import messages
from .models import user_reg,user_log

def index(request):
    return render(request,"index.html")

def admin(request):
    return render(request,"admin.html")

def login(request):
    return render(request,"login.html")

def UserReg(request):
     if request.method=="POST":
         form=user_reg(request.POST)
         login=user_log(request.POST)
         if form.is_valid() and login.is_valid():
             user=user_log.save(commit=False)
             user.usertype="1"
             u=user_reg(commit=False)
             u.userid=user
             u.save()
             messages.success(request,"user registration successfull")
     else:
         form=user_reg()
         login=user_log()
     return render(request,'registration.html',{'form':form,'login':login})
# Create your views here.
