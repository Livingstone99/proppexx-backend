from django.contrib import admin
from .models import Verification
# Register your models here.


class VerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at',)
    list_display_links = ('user',)


admin.site.register(Verification, VerificationAdmin)
