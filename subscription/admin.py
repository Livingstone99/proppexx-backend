from django.contrib import admin
from .models import MembershipPlanFeatures, MembershipPlan
# Register your models here.

admin.site.register(MembershipPlanFeatures)
admin.site.register(MembershipPlan)
# admin.site.register(Subscription)
