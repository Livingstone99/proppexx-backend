from django.urls import path
from . import views

urlpatterns = [
    path('add', views.CreatePropertyRequestApiViewSet.as_view(), name='add-property-request'
         ),
    path('detail/<int:id>', views.PropertyRequestDetailView.as_view({'get': 'retrieve'})
         ),
    path('all', views.PropertyRequestList.as_view()
         ),
]
