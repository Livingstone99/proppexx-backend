from django.contrib import admin
from .models import Property, PropertyType,  Feature, Report
from property.models import PropertyImage
# Register your models here.
from django.contrib.gis.admin import OSMGeoAdmin


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage


class PropertyAdmin(OSMGeoAdmin):
    inlines = [
        PropertyImageInline,
    ]
    list_display = ('title', 'price', 'active',)
    list_display_links = ('title', )


class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at',)
    list_display_links = ('user', )


admin.site.register(Property, PropertyAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(PropertyType)
admin.site.register(Feature)
# admin.site.register(Feature)
