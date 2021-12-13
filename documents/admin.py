from django.contrib import admin
from .models import Documents


# Register your models here.

class DocumentsModels(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at', 'updated_at',)

admin.site.register(Documents, DocumentsModels)