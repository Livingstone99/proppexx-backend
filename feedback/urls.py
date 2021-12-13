from django.urls import path
from . import views

urlpatterns = [
    path('list-feedback',
         views.ListUserFeedbackViewset.as_view(), name='admin-list-feedback'),
    path('send-feedback', views.CreateFeedbackViewset.as_view(), name='user-feedback'),
    path('reply-feedback/<int:pk>',
         views.Admin_reply_to_feedback_view, name='admin-feedback'),
]
