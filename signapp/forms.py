from django import forms
from .models import user_reg,user_log

class userreg(forms.ModelForm):
  class Meta:
    model=user_reg
    fields = ['Name','Gender','Contact']

class userlog(forms.ModelForm):
  class Meta:
    model=user_log
    fields = ['Email','Password']

class logincheck(forms.Form):
    Email = forms.EmailField()
    Password = forms.CharField(max_length='100',widget=forms.PasswordInput)