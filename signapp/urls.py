from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name="index"),
    path('admin_home/',views.admin,name="admin"),
    path('loginpage/',views.UserLogin,name="login"),
    path('registration/',views.UserReg,name="UserReg"),
    path('edit_profile/',views.EditUser,name="EditUser"),
    path('admin_usertable/',views.admin_userview,name="admin_usertable"),
    path('admin_grptable/',views.admin_grpview,name="admin_grptable"),
    path('user_feedback/',views.user_feeds,name="user_feedback"),
    
    path('meetings/',views.meetings,name="meetings"),
    path('video/<int:user_id>/',views.video,name="video"),
    path('user_in/',views.user_in,name="user_in"),
    path('change_pass/',views.change_userpass,name="change_userpass"),
    path('logout/',views.logout,name="logout"),

    path('community_admin/',views.community_admin,name="community_admin"),

    path('view_community/',views.view_community,name="view_community"),
    path('edit_community/<int:community_id>/', views.edit_community, name="edit_community"),
    path('delete_community/<int:community_id>/', views.delete_community, name="delete_community"),
    path('del_community/<int:community_id>/',views.del_community,name="del_community"),

    path('view_user/<int:community_id>/',views.view_user,name="view_user"),
    path('add_member/<int:community_id>/<int:user_id>/',views.add_member,name="add_member"),
    path('view_member/<int:community_id>/',views.view_member,name="view_member"),
    path('delete_member/<int:community_id>/<int:cmid>/',views.delete_member,name="delete_member"),
    path('delete_user/<int:user_id>/',views.delete_user,name="delete_user"),

    path('chat/<int:community_id>/',views.chats,name="chat"),
    path('community/',views.community,name="community"), 
    path('exitgroup/<int:community_id>/',views.exit_group,name="exit_group"),
    path('save_video_url/<int:id>/',views.save_video_url,name="save_video_url"),
    

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    
    path('feedback/', views.submit_feedback, name='feedback'),
    path('logouts/', views.logouts, name='logouts'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)