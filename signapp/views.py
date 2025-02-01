from django.shortcuts import render,redirect,get_object_or_404
from .forms import userreg,userlog,logincheck
from django.contrib import messages
from .models import user_reg,user_log
# Create your views here.


def index(request):
    return render(request,"index.html")

def admin(request):
    return render(request,"admin.html")

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
        form=logincheck(request.POST)
        if form.is_valid():
            email=form.cleaned_data['Email']
            password=form.cleaned_data['Password']
            try:
                user=user_log.objects.get(Email=email)
                if user.Password==password:
                    if user.usertype==1:
                        request.session['user_id']=user.id
                        return redirect('user_in')
                    
                else:
                    messages.success(request,'invalid password')
            except user_log.DoesNotExist:
                messages.error(request,"User doesn't exist ")
    else:
        form=logincheck()
    return render(request,'login2.html',{'form':form})


def EditUser(request):
    id=request.session['user_id']
    user=get_object_or_404(user_log, id=id)
    register= get_object_or_404(user_reg, userid=user)
    if request.method=="POST":
         form=userreg(request.POST,instance=register)
         login=userlog(request.POST,instance=user)
         if form.is_valid() and login.is_valid():
            form.save()
            login.save()
            messages.success(request,"profile updated successfull")
            return redirect('index')
    else:
         form=userreg(instance=register)
         login=userlog(instance=user)
    return render(request,'edit_profile.html',{'form':form,'login':login})

def admin_userview(request):
    user=user_reg.objects.all()
    return render(request,'admin_userview.html',{'user':user})

def meetings(request):
    current_user = request.user
    users = user_reg.objects.exclude(id=current_user.id)
    return render(request, 'meetings.html', {'users': users})

def video(request):
    return render(request,"videocall.html")

def user_in(request):
    return render(request,"user_in.html")