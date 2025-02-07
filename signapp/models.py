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

class community_tab(models.Model):
  community_name=models.CharField(max_length=50)
  community_desc=models.CharField(max_length=350)
  community_logo=models.FileField(upload_to='uploads/')
  userid=models.ForeignKey(user_log,on_delete=models.CASCADE)

