from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# Forms and Models
from .forms import *
from .models import *

# forget password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail


# Utilities
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone


# MY VIEWS 👇🏻


# app main page
def index(request):
    return render(request,"index.html")

# Admin page
def admin(request):
    return render(request,"admin.html")

# User Registration
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

#  User Login
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
                    elif user.usertype==0:
                        request.session['user_id']=user.id
                        return redirect('admin')
                    
                else:
                    messages.success(request,'invalid password')
            except user_log.DoesNotExist:
                messages.error(request,"User doesn't exist ")
    else:
        form=logincheck()
    return render(request,'login2.html',{'form':form})

# Edit user profile
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
    return render(request,'edit_profile.html',{'form':form,'login':login,'register':register})

# view all users by admin
def admin_userview(request):
    user=user_reg.objects.all()
    return render(request,'admin_userview.html',{'user':user})

def admin_grpview(request):
    group=community_tab.objects.all()
    return render(request,'admin_grpview.html',{'group':group})

def user_feeds(request):
    feedbacks=Feedback.objects.all()
    return render(request,'user_feedbacks.html',{'feeds':feedbacks})

# views users for meeting
def meetings(request):
    current_user = request.session.get('user_id')
    users = user_reg.objects.exclude(id=current_user)
    register=get_object_or_404(user_reg,userid=current_user)
    return render(request, 'meetings.html', {'users': users,'register':register})

# video call 
def video(request,user_id):
    users=get_object_or_404(user_reg,id=user_id)
    # user = user_reg.objects.exclude(id=users.id)
    return render(request,"videocall.html",{'user':users})
    # return render(request,"videocall.html")

# user page
def user_in(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(user_reg, userid=user_id)
    return render(request,"user_in.html",{'user':user})


# change password
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

# Logout
# def logout(request):
#     submit_feedback()
#     request.session.flush()
#     messages.success(request, 'You have been logged out successfully.')
#     return redirect('login')

def logouts(request):
    
    
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')
def logout(request):
    # Check if user is logged in
    if not request.session.get('user_id'):
        return redirect('login')
    
    # Redirect to feedback form first
    return redirect('feedback')


# create community
def community_admin(request):
    user_id = request.session.get('user_id') 
    logdata=get_object_or_404(user_log,id=user_id)
    
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
    register = get_object_or_404(user_reg, userid=logdata)

    communities = community_tab.objects.filter(userid=logdata) 
    return render(request, 'view_community.html', {'communities': communities, 'register': register})



# Edit Community
def edit_community(request, community_id):
    user=request.session.get('user_id')
    register=get_object_or_404(user_reg,userid=user)
    community = get_object_or_404(community_tab, id=community_id)
    if request.method == "POST":
        form = community_form(request.POST, request.FILES, instance=community)
        if form.is_valid():
            form.save()
            messages.success(request, "Community updated successfully!")
            return redirect('view_community')
    else:
        form = community_form(instance=community)
    return render(request, 'edit_community.html', {'form': form, 'community': community,'register':register})

# Delete Community
def delete_community(request, community_id):
    community = get_object_or_404(community_tab, id=community_id)
    # if request.method == "POST":
    community.delete()
        # messages.success(request, "Community deleted successfully!")
    return redirect('view_community')
    # return render(request, 'delete_community.html', {'community': community})

# view all users
def view_user(request,community_id):
    current_user = request.session.get('user_id')
    comm_id=community_tab.objects.get(id=community_id)
    users = user_reg.objects.exclude(id=current_user)
    mem=community_member.objects.filter(community_id=comm_id)
    member_ids = mem.values_list('member_id', flat=True)
    return render(request, 'view_user.html', {'users': users,'comm_id':comm_id,'mem':member_ids})

# #add member demo
def add_member(request, community_id, user_id):
    user=request.session.get('user_id')
    comm_id = community_tab.objects.get(id=community_id)
    useid = user_log.objects.get(id=user_id)
    community_admin = request.session.get('user_id')
    admin_id = user_log.objects.get(id=community_admin)
    register=get_object_or_404(user_reg,userid=user)
    # Add the admin as a member if not already added
    if not community_member.objects.filter(community_id=comm_id, member_id=admin_id).exists():
        community_member.objects.create(community_id=comm_id, admin_id=admin_id, member_id=admin_id)
    # Add the new member
    add_mem = community_member.objects.create(community_id=comm_id, admin_id=admin_id, member_id=useid)
    return redirect('view_user', community_id=community_id)
    # return render(request, 'view_user.html', {'comm_id': community_id, 'register': register,'admin_id':admin_id,'useid':useid,'add_mem':add_mem})


# view Community member demo
def view_member(request, community_id):
    user=request.session.get('user_id')
    comm = community_member.objects.filter(community_id=community_id).select_related('member_id__member_userid')
    print(comm)
    members = user_reg.objects.filter(userid__in=comm.values_list('member_id', flat=True))
    register=get_object_or_404(user_reg,userid=user)
    # Fetch the admin
    admin_id = comm.first().admin_id if comm.exists() else None
    admin = user_reg.objects.filter(userid=admin_id).first() 
    return render(request, 'view_members.html', {'comm': comm, 'members': members, 'admin': admin,'register':register})



# Delete Community
# def delete_member(request, community_id,cmid):--
#     member = get_object_or_404(community_member, id=cmid)--
#     member.delete()--
        # messages.success(request, "Community deleted successfully!")
    # return redirect('view_member',community_id=community_id)  -----
    # return render(request, 'delete_member.html', {'member': member})

def delete_member(request, community_id, cmid):
    # Get the current logged-in user
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    # Get the community member to be deleted
    member = get_object_or_404(community_member, id=cmid)
    community = get_object_or_404(community_tab, id=community_id)

    # Check if the logged-in user is the admin of the community
    if member.admin_id.id != user_id:
        messages.error(request, "You are not authorized to remove members from this community.")
        return redirect('view_member', community_id=community_id)

    # Delete the member
    member.delete()

    # Success message after deletion
    messages.success(request, "Member removed successfully.")
    return redirect('view_member', community_id=community_id)





#demo chat
# def chats(request, community_id):
#     user_id = request.session.get('user_id')  # Get the logged-in user
#     if not user_id:
#         return redirect('login')

#     usergg = get_object_or_404(user_log, id=user_id)
#     community = get_object_or_404(community_tab, id=community_id)

#     # Fetch member count for the current community
#     member_count = community_member.objects.filter(community_id=community).count()
#     comm = community_member.objects.filter(community_id=community).select_related('member_id__member_userid')
#     print(comm)
#     # Fetch all communities the user is a member of, an admin of, or has created
#     member_communities = community_member.objects.filter(member_id=usergg).values_list('community_id', flat=True)
#     admin_communities = community_member.objects.filter(admin_id=usergg).values_list('community_id', flat=True)
#     created_communities = community_tab.objects.filter(userid=usergg).values_list('id', flat=True)
#     all_community_ids = set(member_communities) | set(admin_communities) | set(created_communities)
#     all_communities = community_tab.objects.filter(id__in=all_community_ids)

#     if request.method == "POST":
#         form = UserChatForm(request.POST)
#         if form.is_valid():
#             chat = form.save(commit=False)
#             chat.sender_id = usergg
#             chat.receiver_id = community
#             chat.save()
#             messages.success(request, "Message sent successfully")
#             return redirect('chat', community_id=community_id)
#     else:
#         form = UserChatForm()

#     # Fetch chat history
#     messages_list = UserChat.objects.filter(receiver_id=community).order_by('date', 'time')

#     return render(request, 'groupchat.html', {
#         'form': form,
#         'messages': messages_list,
#         'community': community,
#         'user': usergg,
#         'member_count': member_count,
#         'all_communities': all_communities,
#         'comm' :comm # Pass the combined queryset
#     })

# demo_chat_2

def chats(request, community_id):
    user_id = request.session.get('user_id')  # Get the logged-in user
    if not user_id:
        return redirect('login')

    usergg = get_object_or_404(user_log, id=user_id)
    community = get_object_or_404(community_tab, id=community_id)

    # Fetch member count for the current community
    member_count = community_member.objects.filter(community_id=community).count()
    comm = community_member.objects.filter(community_id=community).select_related('member_id__member_userid')
    # print(comm)
    # Fetch all communities the user is a member of, an admin of, or has created
    member_communities = community_member.objects.filter(member_id=usergg).values_list('community_id', flat=True)
    admin_communities = community_member.objects.filter(admin_id=usergg).values_list('community_id', flat=True)
    created_communities = community_tab.objects.filter(userid=usergg).values_list('id', flat=True)
    all_community_ids = set(member_communities) | set(admin_communities) | set(created_communities)
    all_communities = community_tab.objects.filter(id__in=all_community_ids)

    if request.method == "POST":
        form = UserChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.sender_id = usergg
            chat.receiver_id = community

            # Check if there's a reply
            # reply_to_id = request.POST.get('reply_to_id')
            # if reply_to_id:
            #     chat.reply_to_id = UserChat.objects.get(id=reply_to_id)  # Set the reply_to field to the actual message object 
            
            reply_to_id = request.POST.get('reply_to_id')
            if reply_to_id:
                try:
                    chat.reply_to = UserChat.objects.get(id=reply_to_id)
                except UserChat.DoesNotExist:
                    chat.reply_to = None  # Handle invalid reply IDs gracefully



            chat.save()
            messages.success(request, "Message sent successfully")
            return redirect('chat', community_id=community_id)
    
    else:
        form = UserChatForm()

    # Fetch chat history
    messages_list = UserChat.objects.filter(receiver_id=community).order_by('date', 'time')

    # Group messages by date
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    grouped_messages = {}
    for message in messages_list:
        if message.date == today:
            date_label = "Today"
        elif message.date == yesterday:
            date_label = "Yesterday"
        else:
            date_label = message.date.strftime("%Y-%m-%d")
        if date_label not in grouped_messages:
            grouped_messages[date_label] = []
        grouped_messages[date_label].append(message)

    return render(request, 'groupchat.html', {
        'form': form,
        'grouped_messages': grouped_messages,
        'community': community,
        'user': usergg,
        'member_count': member_count,
        'all_communities': all_communities,
        'comm' :comm # Pass the combined queryset
    })



def community(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login') 
    user = get_object_or_404(user_log, id=user_id)
    register = get_object_or_404(user_reg, userid=user)
    # Fetch all community IDs where the user is a member, admin, or creator
    member_community_ids = community_member.objects.filter(member_id=user,user_status=0).values_list('community_id', flat=True )
    admin_community_ids = community_member.objects.filter(admin_id=user,user_status=0).values_list('community_id', flat=True )
    created_community_ids = community_tab.objects.filter(userid=user).values_list('id', flat=True)
    # Combine all community IDs
    all_community_ids = set(member_community_ids) | set(admin_community_ids) | set(created_community_ids)
    # Fetch the actual community objects
    all_communities = community_tab.objects.filter(id__in=all_community_ids)
    if not all_communities.exists():
        messages.info(request, "You are not a member of any community and have not created any communities!")
    return render(request, 'community.html', {'communities': all_communities, 'user': user, 'register': register})


def exit_group(request, community_id):
    print(community_id)
    user_id = request.session.get('user_id')
    user = get_object_or_404(user_log, id=user_id)
    community = get_object_or_404(community_tab, id=community_id)
    print(community)
    # Check if the user is an admin
    is_admin = community_member.objects.filter(community_id=community, admin_id=user).exists()
    # Check if the user is a member
    is_member = community_member.objects.filter(community_id=community, member_id=user).exists()
    if is_admin:
        # Delete the community if the user is the admin
        community.delete()
        messages.success(request, "Community deleted successfully!")
    elif is_member:
        # Remove the user from the community if they are a member
        communitys=community_member.objects.filter(community_id=community, member_id=user).first()
        print(communitys)
        communitys.user_status = 1
        communitys.save()
        messages.success(request, "You have exited the community successfully!")
    else:
        messages.error(request, "You are not a member of this community!")
    return redirect('community')

@csrf_exempt  
def save_video_url(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data.get('url')

        if url:
            appointment = get_object_or_404(user_reg, id=id)
            
            appointment.meet = url
            
            appointment.save()

            return JsonResponse({'success': True, 'message': 'URL saved successfully'})

        return JsonResponse({'success': False, 'message': 'No URL provided'}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

# Forgot Password View
# def forgot_password(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         try:
#             user = user_log.objects.get(Email=email)
#             token = default_token_generator.make_token(user)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             reset_link = request.build_absolute_uri(
#                 f'/reset-password/{uid}/{token}/'
#             )
#             send_mail(
#                 subject="Password Reset Request",
#                 message=f"Click the link to reset your password: {reset_link}",
#                 from_email='your_email@gmail.com',  # Replace with your Gmail address
#                 recipient_list=[email],
#             )
#             messages.success(request, "Password reset link sent to your email.")
#         except user_log.DoesNotExist:
#             messages.error(request, "No account found with this email.")
#     return render(request, 'forgot_password.html')


# def forgot_password(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         try:
#             user = user_log.objects.get(Email=email)
#             token = default_token_generator.make_token(user)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             reset_link = request.build_absolute_uri(f'/reset-password/{uid}/{token}/')

#             # Send the email
#             try:
#                 send_mail(
#                     subject="Password Reset Request",
#                     message=f"Hi,\n\nClick the link below to reset your password:\n{reset_link}\n\nIf you didn’t request this, ignore this email.",
#                     from_email='signify4u@gmail.com',  # Must match your settings.py email config
#                     recipient_list=[email],
#                     fail_silently=False,
#                 )
#                 messages.success(request, "Password reset link sent to your email.")
#             except Exception as e:
#                 messages.error(request, f"Email sending failed: {str(e)}")
#         except user_log.DoesNotExist:
#             messages.error(request, "No account found with this email.")

#     return render(request, 'forgot_password.html')
# # views.py
import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = user_log.objects.get(Email=email)
            otp = str(random.randint(100000, 999999))
            request.session['reset_email'] = email
            request.session['reset_otp'] = otp

            send_mail(
                'Your OTP for Password Reset',
                f'Your OTP is: {otp}',
                'signify4u@gmail.com',  # From
                [email],           # To
                fail_silently=False,
            )

            return redirect('verify_otp')
        except User.DoesNotExist:
            messages.error(request, 'Email not registered.')
    return render(request, 'forgot_password.html')

# views.py
def verify_otp_view(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == request.session.get('reset_otp'):
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'verify_otp.html')
def reset_password_view(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            email = request.session.get('reset_email')
            user = user_log.objects.get(Email=email)
            user.Password = password
            user.save()

            # Clean up session
            request.session.flush()

            messages.success(request, 'Password reset successful!')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
    return render(request, 'resets_password.html')
# Reset Password View
# def reset_password(request, uidb64, token):
#     if request.method == 'POST':
#         new_password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
#         if new_password == confirm_password:
#             try:
#                 uid = force_str(urlsafe_base64_decode(uidb64))
#                 user = user_log.objects.get(pk=uid)
#                 if default_token_generator.check_token(user, token):
#                     user.Password = new_password  # Save the new password
#                     user.save()
#                     messages.success(request, "Password updated successfully.")
#                     return redirect('login')  # Redirect to your login page
#                 else:
#                     messages.error(request, "Invalid token or link expired.")
#             except Exception as e:
#                 messages.error(request, "Something went wrong.")
#         else:
#             messages.error(request, "Passwords do not match.")
#     return render(request, 'reset_password.html')



def submit_feedback(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')  
    logdata = get_object_or_404(user_log, id=user_id)
    register = get_object_or_404(user_reg, userid=logdata)
    
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.login_id = logdata
            feedback.save()
            messages.success(request, "Thank you for your feedback. You have been logged out.")
            
            # Logout after feedback
            request.session.flush()
            return redirect('../loginpage/')
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form,'register':register})

# def view_received_calls(request):
#     received_calls = meetings.objects.filter(receiver=request.user).order_by('-created_at')
#     return render(request, 'noti.html', {'received_calls': received_calls})
