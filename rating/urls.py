from django.urls import path
from . import views


urlpatterns = [
     path('rate_agent',views.AgentRatingApiViewSet.as_view(), name = 'rate_agent' ),
     path('<int:id>', views.AllRatingsPerAgentAPIViewSet.as_view(), name = 'agent_rating'),
     path('all-rating', views.AllRatingApiViewSet.as_view(), name = 'all_ratings'),
     path('get-a-rating/<int:id>', views.RatingRetrieveApiViewSet.as_view(), name = 'single_rating')
     # path('')
]