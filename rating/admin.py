from django.contrib import admin

# Register your models here.
from .models import AgentRating


class AgentRatingAdmin(admin.ModelAdmin):
    list_display = [
        'buyer_user', 
        'agent_user',
        'rate'
    ]
    list_display_links = [
        'buyer_user',
    ]
admin.site.register(AgentRating, AgentRatingAdmin)
