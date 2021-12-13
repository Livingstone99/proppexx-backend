from django.urls import path
from . import views



urlpatterns = [
    path('property-review', views.RequestReviewApiViewSet.as_view()),
    path('review-list', views.RequestListApiViewSet.as_view()),
    path('on-success/<int:review_id>', views.ConfirmPropReviewViewSet.as_view()),
    path('all-review', views.AllRequestApiViewSet.as_view()),
    path('assign-agent/<int:review_id>', views.AssignAgentApiViewSet.as_view()),
    path('<int:review_id>', views.RetrieveReviewViewSet.as_view()),

   
]
