from django.contrib import admin
from .models import Article
# Register your models here.



class ArticleAdmin(admin.ModelAdmin):
    list_display = ('writer', 'title', 'display')
    list_display_links = ('title', )
admin.site.register(Article)