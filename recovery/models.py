from django.db import models
from django.conf import settings
from items.models import Item


class Match(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('REJECTED', 'Rejected'),
    ]

    lost_item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='lost_matches'
    )

    found_item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='found_matches'
    )

    match_score = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('lost_item', 'found_item')

    def __str__(self):
        return f'{self.lost_item.title} - {self.found_item.title}'


class ClaimRequest(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='claims'
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='claim_requests'
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student} - {self.match}'


class Verification(models.Model):

    claim = models.ForeignKey(
        ClaimRequest,
        on_delete=models.CASCADE,
        related_name='verifications'
    )

    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    decision = models.CharField(
        max_length=10,
        choices=[
            ('APPROVED', 'Approved'),
            ('REJECTED', 'Rejected'),
        ]
    )

    remarks = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.claim} - {self.decision}'


