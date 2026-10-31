from django.contrib import admin
from .models import Match, ClaimRequest, Verification, Notification

# Register your models here.
admin.site.register(Match)
admin.site.register(ClaimRequest)
admin.site.register(Verification)
admin.site.register(Notification)