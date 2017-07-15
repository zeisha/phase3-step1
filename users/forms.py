from django import forms
from .models import User

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')



class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields= (
            'username', 'password', 'first_name', 'last_name', 'email'
        )
