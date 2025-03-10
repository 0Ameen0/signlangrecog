from django.db import models


# Create your models here.

class user_log(models.Model):
  Email=models.EmailField(unique=True)
  Password=models.CharField(max_length=100)
  usertype=models.IntegerField(default=0)

class user_reg(models.Model):
  Name=models.CharField(max_length=100)
  Gender=models.CharField(max_length=50)
  Contact=models.CharField(max_length=15)
  userid=models.ForeignKey(user_log,on_delete=models.CASCADE)
  img=models.FileField(upload_to='uploads/',default=True)

class community_tab(models.Model):
  community_name=models.CharField(max_length=50)
  community_desc=models.CharField(max_length=350)
  community_logo=models.FileField(upload_to='uploads/')
  userid=models.ForeignKey(user_log,on_delete=models.CASCADE)

class community_member(models.Model):
  community_id=models.ForeignKey(community_tab,on_delete=models.CASCADE)
  admin_id=models.ForeignKey(user_log,on_delete=models.CASCADE,related_name='admin_id')
  member_id=models.ForeignKey(user_log,on_delete=models.CASCADE,related_name='member_id')
  date = models.DateTimeField(auto_now_add=True)

class UserChat(models.Model):
    sender_id = models.ForeignKey(user_log, on_delete=models.CASCADE)
    receiver_id = models.ForeignKey(community_tab, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

