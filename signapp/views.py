from django.shortcuts import render,redirect,get_object_or_404
from .forms import userreg,userlog,logincheck,user_edit
from django.contrib import messages

from django.contrib.auth.decorators import login_required
# from django.contrib.auth.hashers import check_password, make_password

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
         login=user_edit(request.POST,instance=user)
         if form.is_valid() and login.is_valid():
            form.save()
            login.save()
            messages.success(request,"profile updated successfull")
            return redirect('user_in')
    else:
         form=userreg(instance=register)
         login=user_edit(instance=user)
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



def change_userpass(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(user_log, id=user_id)

    if request.method == "POST":
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Display current password for debugging purposes (remove after verification)
        print(f"Current password in database: {user.Password}")

        # Direct password comparison (plain text)
        if current_password != user.Password:
            messages.error(request, 'Invalid current password.')
            return redirect('change_userpass')

        # Validate new password confirmation
        if new_password != confirm_password:
            messages.error(request, 'New password and confirmation do not match.')
            return redirect('change_userpass')

        # Save new password directly (no hashing)
        user.Password = new_password
        user.save()

        messages.success(request, f'Password changed successfully!')
        return redirect('EditUser')

    return render(request, 'change_userpass.html')


def logout(request):
    # Clear the session to log the user out
    request.session.flush()  # This clears all session data

    # Add a logout success message
    messages.success(request, 'You have been logged out successfully.')

    # Redirect to the login page (replace 'login' with your login URL name)
    return redirect('login')