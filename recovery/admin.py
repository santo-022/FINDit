from django.contrib import admin
from .models import Match, ClaimRequest, Verification

# Register your models here.
admin.site.register(Match)
admin.site.register(ClaimRequest)
admin.site.register(Verification)