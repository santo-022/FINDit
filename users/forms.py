from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Student, Staff


class StudentRegisterForm(UserCreationForm):
    class Meta:
        model = Student
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'phone_number', 'profile_picture', 'id_card',
            'department', 'section', 'batch'
        ]


class StaffRegisterForm(UserCreationForm):
    class Meta:
        model = Staff
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'phone_number', 'profile_picture', 'id_card'
        ]


class LoginForm(AuthenticationForm):

    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login':"Invalid username or password, or your account "
                         "has not been verified by the admin yet.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password',
        })


