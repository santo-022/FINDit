from django import forms
from django.contrib.auth.forms import UserCreationForm
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