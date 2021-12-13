from django.contrib import admin
from .models import BookmarkProperty
# Register your models here.


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id','buyer',)
    list_display_links = ('id',)

admin.site.register(BookmarkProperty, BookmarkAdmin)