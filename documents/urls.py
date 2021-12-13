from django.urls import path
from . import views


urlpatterns = [
    path('add-document', views.UpdateDocumentApiViewSet.as_view(), name='add_document'),
    path('document-list', views.AllAgentsDocumentApiViewSet.as_view(),
         name='all_documents'),
    path('agent-document', views.AgentRetrieveDocumentApiViewSet.as_view(),
         name='agent_document'),
    path('verify-document/<int:agent_id>',
         views.CheckDocumentApiViewSet.as_view(), name='check_document'),
    path('check-activation-status', views.activation_status_check,
         name='check_activation_status'),
]
