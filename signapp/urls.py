from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('admin_home/',views.admin,name="admin"),
    path('loginpage/',views.UserLogin,name="login"),
    path('registration/',views.UserReg,name="UserReg"),
    path('edit_profile/',views.EditUser,name="EditUser"),
    path('admin_usertable/',views.admin_userview,name="admin_userview"),
    path('meetings/',views.meetings,name="meetings"),
    path('video/',views.video,name="video"),
    path('user_in/',views.user_in,name="user_in"),
    path('change_pass/',views.change_userpass,name="change_userpass")
]