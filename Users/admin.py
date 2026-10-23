from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student, Staff


@admin.register(Student)
class StudentAdmin(UserAdmin):
    list_display = ('username', 'email', 'department', 'batch', 'is_active')
    list_filter = ('is_active', 'department', 'batch')

    # fields shown when editing an existing student
    fieldsets = UserAdmin.fieldsets + (
        ('Extra info', {'fields': ('phone_number', 'facebook_id', 'profile_picture', 'id_card')}),
        ('Student info', {'fields': ('department', 'section', 'batch')}),
    )
    # fields shown on the "Add student" page
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Extra info', {'fields': ('phone_number', 'facebook_id', 'profile_picture', 'id_card')}),
        ('Student info', {'fields': ('department', 'section', 'batch')}),
    )


@admin.register(Staff)
class StaffAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_active')
    list_filter = ('is_active',)

    fieldsets = UserAdmin.fieldsets + (
        ('Extra info', {'fields': ('phone_number', 'facebook_id', 'profile_picture', 'id_card')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Extra info', {'fields': ('phone_number', 'facebook_id', 'profile_picture', 'id_card')}),
    )