from django.urls import path
from rest_framework.decorators import api_view
from . import views


urlpatterns = [

    path('property-type', views.PropertyTypeApiViewSet.as_view(), name='type'
         ),
     path('prop-availability/<int:property_id>', views.property_availability),
    path('feature', views.FeatureApiViewSet.as_view(), name='feature'
         ),

    path('property_type/<int:id>', views.PropertyTypeUpdateApiViewSet.as_view(), name='type_id'
         ),
    path('feature/<int:id>', views.FeatureUpdateApiViewSet.as_view(), name='feature_id'
         ),
    path('add', views.AddPropertyApiViewSet.as_view(), name='add_property'
         ),
    path('agent-property/<int:user_id>',
         views.AgentPropertyList.as_view(), name='agent_property'),
     path('town-based/<str:town>',
         views.PropertyListBaseOnTown.as_view(), name='town_based'),
    path('property-list', views.AllPropertiesApiViewSet.as_view(),
         name="all_properties"),
    path('property-type-list', views.PropertyTypeListView.as_view(),
         name="all_propertiestype"),
    path('property-feature-list', views.PropertyFeatureListView.as_view(),
         name="all_propertiesfeature"),
    path('edit/<int:property_id>',
         views.PropertyUpdateViewSet.as_view(), name='property_id'),
    path('agent-property', views.PropertyListOnResquestApiViewSet.as_view(),
         name='get_on_request'),
    path('detail/<int:id>',
         views.PropertyDetailsReadOnlyApiViewSet.as_view(), name='detail'),
    path('flag/<int:property_id>', views.flag_property, name='flag_property'),
    path('unpublish/<int:property_id>',
         views.unpublish_property, name='unpublish_property'),
    path('sold/<int:property_id>',
         views.property_sold, name='sold_property'),

    path('property-count', views.property_count, name='property_count'),
    path('nearest-property/<str:lat>/<str:long>', views.NearestPropertyToLocation.as_view(),
         name='get_nearest_properties'),
    path('add-report', views.CreateReportApiViewSet.as_view(), name='report'),
    path('retrieve-report/<int:report_id>',
         views.RetrieveReportApiViewSet.as_view(), name='retrieve_report'),
    path('all-reports', views.ReportListApiViewSet.as_view(), name='all_reports'),
    path('reports-per-property/<int:property_id>',
         views.ReportsPerPropertyApiViewSet.as_view(), name='reports_per_property'),
     path('update-status/<int:property_id>', views.StatusUpdateApiViewSet.as_view(), name = 'update_status'),
     path('add-to-draft',views.CreateDraftApiViewSet.as_view(), name = 'draft' ),
     path('draft/<int:draft_id>', views.DraftUpdateviewSet.as_view(), name = 'update-draft'),
     path('draft-list', views.AllAgentDraftViewSet.as_view(), name = 'draaft-list'),
     path('property-distance/<str:lat>/<str:long>', views.distance_nearest_property, name= 'property-distance'),
    path('search-base-on-geodata/<str:lat>/<str:long>/<str:purpose>', views.SearchPropertyUsingGeoDataViewset.as_view(), name = 'geo_search'),
    path('properties-in-prominient-cities/<str:lat>/<str:long>', views.SearchPropertyInProminientCityViewset.as_view(), name = 'prominient_city'),
    path('demographics/<str:state>', views.stateAPI, name= 'state-api'),
]
