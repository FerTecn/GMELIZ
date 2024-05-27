from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class SignupForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices=[('Cliente', 'Cliente'), ('Vendedor', 'Vendedor')],
        widget=forms.Select(attrs={'class': 'form-control blurInput'}),
      
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
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


    def _init_(self,args,*kwargs):
        super()._init_(*args, **kwargs)
        
        for field in self.fields.values():
            field.help_text = ''

        self.fields['username'].widget.attrs.update({'class': 'form-control form-control-user blurInput'})
        self.fields['password'].widget.attrs.update({'class': 'form-control form-control-user blurInput'})