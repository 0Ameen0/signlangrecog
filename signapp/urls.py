from django.urls import path
from . import views

urlpatterns = [
    path('index',views.index,name="index"),
    path('admin_home/',views.admin,name="admin"),
    path('loginpage/',views.UserLogin,name="login"),
    path('registration/',views.UserReg,name="UserReg"),
    path('edit_profile/',views.EditUser,name="EditUser"),
    path('admin_usertable',views.admin_userview,name="admin_userview")
]