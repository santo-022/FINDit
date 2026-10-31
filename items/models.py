from django.db import models
from django.conf import settings


class Catagory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Item(models.Model):

    TYPE_CHOICES = [
        ('LOST', 'Lost'),
        ('FOUND', 'Found'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('MATCHED', 'Matched'),
        ('CLAIMED', 'Claimed'),
        ('RESOLVED', 'Resolved'),
        ('REJECTED', 'Rejected'),
    ]

    title = models.CharField(max_length=100)
    catagory = models.ForeignKey(Catagory, on_delete=models.PROTECT)
    description = models.TextField(max_length=300)
    picture = models.ImageField(upload_to='item_pics/', blank=True, null=True)
    color = models.CharField(max_length=15)
    brand = models.CharField(max_length=20)
    location = models.CharField(max_length=80)
    incident_d_t = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    itemtype = models.CharField(max_length=5, choices=TYPE_CHOICES, default='LOST')

    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reported_items'
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    def __str__(self):
        return f'{self.itemtype}_{self.title}'