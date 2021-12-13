from django.contrib import admin
from .models import Review

# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ('user', 'property', 'status', 'paid', 'created_at', )
    list_display_links = ('user',)

admin.site.register(Review, ReviewAdmin)
