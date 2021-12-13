from django.urls import path
from . import views


urlpatterns = [
    path('request', views.VerificationRequestApiViewSet.as_view(), name = 'request'),
    path('all-requests', views.GetAllRequestApiViewSet.as_view(), name = 'all_request'),
    path('pending-request', views.GetAllPendingRequestApiViewSet.as_view(), name = 'pending'),
    path('verify-agent/<int:user_id>', views.VerifyingAgentApiViewSet.as_view(), name = 'verify_agent'),
    path('upload-document', views.uploadDocumentApiViewSet.as_view(), name='upload-document')
]
