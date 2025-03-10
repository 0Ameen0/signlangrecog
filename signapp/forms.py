from django import forms
from .models import *

class userreg(forms.ModelForm):
  class Meta:
    model=user_reg
    fields = ['Name','Gender','Contact','img']

class userlog(forms.ModelForm):
  class Meta:
    model=user_log
    fields = ['Email','Password']

class logincheck(forms.Form):
    Email = forms.EmailField()
    Password = forms.CharField(max_length='100',widget=forms.PasswordInput)


class user_edit(forms.ModelForm):
  class Meta:
    model=user_log
    fields = ['Email']


class community_form(forms.ModelForm):
  class Meta:
    model=community_tab
    fields=['community_name','community_desc','community_logo']


class UserChatForm(forms.ModelForm):
    class Meta:
        model = UserChat
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows':2,'placeholder': 'Write your message...'})
        }
