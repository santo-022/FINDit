from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    """
    Because is_active defaults to False, the superuser would be created
    inactive and couldn't log in. This forces superusers to be active.
    """
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    """Base class: everything Student and Staff share."""

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    facebook_id = models.URLField(max_length=300, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    id_card = models.ImageField(upload_to='ID_pics/', blank=False, null=False)

    # Admin must verify identity before the account can log in
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.get_full_name() or self.username}"


class Student(User):
    class Department(models.TextChoices):
        CSE = 'CSE', 'Computer Science & Engineering'
        EEE = 'EEE', 'Electrical & Electronic Engineering'
        BBA = 'BBA', 'Business Administration'
        ENG = 'ENG', 'English'
        LAW = 'LAW', 'Law'
        PHA = 'PHA', 'Pharmacy'
        # add/change to match your campus

    department = models.CharField(max_length=3, choices=Department.choices)
    section = models.CharField(max_length=5)
    batch = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.username} ({self.department}, Batch {self.batch})"
    class Meta:
        verbose_name_plural = 'Student'

class Staff(User):
    """Inherits everything from User. Add staff-only fields here later
    (e.g. designation, office_room)."""
    def __str__(self):
        return f"{self.username})"

    class Meta:
        verbose_name_plural = 'Staff'