from django.contrib import admin
from .models import Feedback
# Register your models here.


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user_from', 'title', 'has_replied')

    fieldsets = [
        ('Feedback',{
         'fields': ["user_from", "message"]}),
        ('Reply', {'fields': ['user_to', 'reply']}),
    ]
