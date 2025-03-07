from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from django.contrib import messages

from django.contrib.auth.decorators import login_required
# from django.contrib.auth.hashers import check_password, make_password

from .models import *
from django.db.models import Q


def index(request):
    return render(request,"index.html")

def admin(request):
    return render(request,"admin.html")

def UserReg(request):
     if request.method=="POST":
         form=userreg(request.POST,request.FILES)
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
         form=userreg(request.POST,request.FILES,instance=register)
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
    current_user = request.session.get('user_id')
    users = user_reg.objects.exclude(id=current_user)
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

        # Direct password comparison 
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
    request.session.flush()
    # logout success message
    messages.success(request, 'You have been logged out successfully.')
    # Redirect to login page
    return redirect('login')

# create community
def community_admin(request):
    user_id = request.session.get('user_id') 
    logdata=get_object_or_404(user_log,id=user_id)
    print("USSSS",logdata)
    if request.method == "POST":
        comm = community_form(request.POST, request.FILES)
        if comm.is_valid():
            form = comm.save(commit=False)
            form.userid=logdata
            form.save()
            messages.success(request, "Community created successfully!")

            return redirect('view_community') 
    else:
        comm = community_form()

    return render(request, 'createcommunity.html', {'comm': comm})

# view community

def view_community(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  
    logdata = get_object_or_404(user_log, id=user_id)
    communities = community_tab.objects.filter(userid=logdata) 
    return render(request, 'view_community.html', {'communities': communities})



# Edit Community
def edit_community(request, community_id):
    community = get_object_or_404(community_tab, id=community_id)

    if request.method == "POST":
        form = community_form(request.POST, request.FILES, instance=community)
        if form.is_valid():
            form.save()
            messages.success(request, "Community updated successfully!")
            return redirect('view_community')
    else:
        form = community_form(instance=community)

    return render(request, 'edit_community.html', {'form': form, 'community': community})

# Delete Community
def delete_community(request, community_id):
    community = get_object_or_404(community_tab, id=community_id)

    # if request.method == "POST":
    community.delete()
        # messages.success(request, "Community deleted successfully!")
    return redirect('view_community')

    # return render(request, 'delete_community.html', {'community': community})

def view_user(request,community_id):
    current_user = request.session.get('user_id')
    comm_id=community_tab.objects.get(id=community_id)
    users = user_reg.objects.exclude(id=current_user)
    mem=community_member.objects.filter(community_id=comm_id)
    member_ids = mem.values_list('member_id', flat=True)

    return render(request, 'view_user.html', {'users': users,'comm_id':comm_id,'mem':member_ids})

def add_member(request,community_id,user_id):

    comm_id=community_tab.objects.get(id=community_id)
    useid=user_log.objects.get(id=user_id)
    community_admin=request.session.get('user_id')
    admin_id=user_log.objects.get(id=community_admin)
    add_mem=community_member.objects.create(community_id=comm_id,admin_id=admin_id,member_id=useid)

    return redirect('view_user',community_id=community_id)

    
def view_member(request, community_id):
    comm = community_member.objects.filter(community_id=community_id).select_related('member_id')
    members = user_reg.objects.filter(userid__in=comm.values_list('member_id', flat=True))

    return render(request, 'view_members.html', {'comm': comm, 'members': members})

# Delete Community
def delete_member(request, community_id,cmid):
    member = get_object_or_404(community_member, id=cmid)
    member.delete()
        # messages.success(request, "Community deleted successfully!")
    return redirect('view_member',community_id=community_id)
    # return render(request, 'delete_member.html', {'member': member})


# Community Chat 
# def chats(request,community_id):
#     user = request.session.get('user_id') # Get the logged-in user
#     community = get_object_or_404(community_tab, id=community_id)  # Get the community
#     usergg = get_object_or_404(user_log, id=user) 
#     # Handle form submission
#     if request.method == "POST":
#         form = UserChatForm(request.POST)
#         if form.is_valid():
#             chat = form.save(commit=False)
#             chat.sender_id = usergg
#             chat.receiver_id = community
#             chat.save()
#             messages.success(request, "Message sent successfully")
#             return redirect('chat',community_id=community_id)
#     else:
#         form = UserChatForm()

#     # Fetch chat history
#     messages_list = UserChat.objects.filter(sender_id=usergg, receiver_id=community).order_by('date','time')

#     return render(request, 'groupchat.html', {'form': form, 'messages': messages_list, 'community': community, 'user': usergg})

def chats(request, community_id):
    user = request.session.get('user_id')  # Get the logged-in user
    community = get_object_or_404(community_tab, id=community_id)  # Get the community
    usergg = get_object_or_404(user_log, id=user)  

    if request.method == "POST":
        form = UserChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.sender_id = usergg
            chat.receiver_id = community  # Message is sent to the community
            chat.save()
            messages.success(request, "Message sent successfully")
            return redirect('chat', community_id=community_id)
    else:
        form = UserChatForm()

    # Fetch chat history (ALL messages related to this community)
    messages_list = UserChat.objects.filter(receiver_id=community).order_by('date', 'time')

    return render(request, 'groupchat.html', {
        'form': form,
        'messages': messages_list,
        'community': community,
        'user': usergg
    })




def community(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login') 
    user = get_object_or_404(user_log,id=user_id)
    community = community_member.objects.filter(member_id=user)

    print(messages) 
    


    if not community.exists():
        messages.info(request, "You are not a member of any community!")

    return render(request, 'community.html', {'community': community , 'user': user})

