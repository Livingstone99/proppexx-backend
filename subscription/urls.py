from django.urls import path
from . import views

urlpatterns = [
    path('membership-plan-add', views.MembershipPlanCreateView.as_view(),
         name='membership-plan-create'),
    path('delete-plan/<int:pk>', views.MembershipPlanDeleteView.as_view(),
         name='delete-plan'),
    path('membership-plan', views.MembershipPlanListView.as_view(),
         name='membership-plan-list'), 
    path('membership-plan-detail/<str:slug>', views.MembershipPlanDetailView.as_view(),
         name='membership-plan'),
    path('initialize-payment/<str:plan_code>', views.InitializeSubscriptionPayment.as_view(),
         name='initialize-payment'),
    path('authorize-subscription/<str:reference>/<str:plan_code>', views.AuthorizeSubscription.as_view(),
         name='authorize-subscription'),
    path('active-subscription', views.GetCurrentSubscription.as_view(),
         name='get-subscription'),
    path('cancel-subscription', views.CancelSubscriptionView.as_view(),
         name='cancel-subscription'),
    path('subscription-list', views.GetAllSubscription.as_view(),
         name='all-subscriptions'),
    path('transaction-list', views.GetAllTransactions.as_view(),
         name='all-subscriptions'),
]
