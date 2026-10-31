from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    facebook_id = models.URLField(max_length=300, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    id_card = models.ImageField(upload_to='ID_pics/', blank=False, null=False)

    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.get_full_name() or self.username}"

    @property
    def is_student(self):
        return hasattr(self, 'student')

    @property
    def is_staff_member(self):
        return hasattr(self, 'staff')

    @property
    def profile(self):
        if self.is_student:
            return self.student
        if self.is_staff_member:
            return self.staff
        return self


class Student(User):
    class Department(models.TextChoices):
        CSE = 'CSE', 'Computer Science & Engineering'
        EEE = 'EEE', 'Electrical & Electronic Engineering'
        BBA = 'BBA', 'Business Administration'
        ENG = 'ENG', 'English'
        LAW = 'LAW', 'Law'
        PHA = 'PHA', 'Pharmacy'
        CIVIL = 'CIV', 'Civil'


    department = models.CharField(max_length=3, choices=Department.choices)
    section = models.CharField(max_length=5)
    batch = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.username} ({self.department}, Batch {self.batch})"
    class Meta:
        verbose_name_plural = 'Student'

class Staff(User):
    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name_plural = 'Staff'