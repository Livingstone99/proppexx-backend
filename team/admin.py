from django.contrib import admin
from .models import AdminAgent, Member, Team  
# Register your models here.

class TeamAdmin(admin.ModelAdmin):
    list_display =  ('first_name',  'last_name', 'email')
    list_display_links = ('first_name', )
    
    
admin.site.register(AdminAgent, TeamAdmin)
admin.site.register(Team)
admin.site.register(Member)