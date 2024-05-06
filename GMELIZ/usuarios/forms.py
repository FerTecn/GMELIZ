from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = '__all__'


    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.help_text = ''

        self.fields['username'].widget.attrs.update({'class': 'form-control form-control-user blurInput'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control form-control-user blurInput'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control form-control-user blurInput'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control form-control-user blurInput'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control form-control-user blurInput'})
        self.fields['email'].widget.attrs.update({'class': 'form-control form-control-user blurInput'})

class SigninForm(AuthenticationForm):

    class Meta:
        model = User
        fields = [
            'username', 
            'password',
            ]


    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.help_text = ''

        self.fields['username'].widget.attrs.update({'class': 'form-control form-control-user blurInput'})
        self.fields['password'].widget.attrs.update({'class': 'form-control form-control-user blurInput'})


    
    