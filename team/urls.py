from django.urls import path
from . import views

urlpatterns = [
    path('create-agent', views.CreateAminAgentViewSet.as_view()),
    path('agent/<int:admin_agent_id>', views.RetrieveAdminAgentViewSet.as_view()),
    path('agent-list', views.ListAdminAgentViewSet.as_view()),
    path('search', views.AgentSearchApiViewSet.as_view()),
    path('create-member', views.MemberRegistrationViewSet.as_view()),
    path('member-list/<int:developer_id>', views.MemberListViewSet.as_view()),
    path('member-list', views.DeveloperMemberList.as_view()),

    path('property-list', views.AgentAssignedPropertyList.as_view()),
    path('property-list-2', views.AgentAssignedPropertyList2.as_view()),
    path('assign/<int:property_id>', views.AssignMemberToPropertyApiViewSet.as_view()),
    path('<int:member_id>', views.UpdateMemberApiViewSet.as_view()),
    path('all-team', views.ListDeveloperTeamApiSerializer.as_view()),
    path('dev-team', views.developer_and_team_list),
    path('active-and-inactive-member/<str:state>', views.active_and_inactive_member)
   
]
