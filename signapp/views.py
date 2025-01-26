from django.shortcuts import render,redirect,get_object_or_404
from .forms import userreg,userlog
from django.contrib import messages
from .models import user_reg,user_log
# Create your views here.


def index(request):
    return render(request,"index.html")

def admin(request):
    return render(request,"admin.html")

def login(request):
    return render(request,"login.html")

def UserReg(request):
     if request.method=="POST":
         form=userreg(request.POST)
         login=userlog(request.POST)
         if form.is_valid() and login.is_valid():
             user=login.save(commit=False)
             user.usertype=1
             user.save()
             u=form.save(commit=False)
             u.userid=user
             u.save()
             messages.success(request,"user registration successfull")
     else:
         form=userreg()
         login=userlog()
     return render(request,'registration.html',{'form':form,'login':login})

def UserLogin(request):
    if request.method=="POST":
        form=userlog(request.POST)
        if form.is_valid():
            email=form.cleaned_data['Email']
            password=form.cleaned_data['Password']
            try:
                user=user_log.objects.get(Email=email)
                if user.Password==password:
                    if user.usertype==1:
                        request.session['user_id']
                        return redirect('index')
                    
                else:
                    messages.success(request,'invalid password')
            except user_log.DoesNotExist:
                messages.error(request,"User doesn't exist ")
    else:
        form=userlog()
    return render(request,'login.html',{'form':form})
  