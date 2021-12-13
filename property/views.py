import re
from django.core.serializers import serialize
import json
from django.db.models import query
from rest_framework import filters
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_gis.filters import DistanceToPointFilter
from django.contrib.gis.db.models.functions import Distance
from geopy.distance import distance as geopy_distance
from django.contrib.gis.measure import Distance as DistanceMeasure
from django.contrib.gis.geos import Point
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, GenericAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from users.permissions import IsAgent, IsAgentOrAdmin, IsAgentOrDeveloper, IsAgentOrDeveloperOrAdmin, IsBuyer
from .serializers import CreateDraftSerializer, DraftSerializer, PropertyTypeSerializer, FeatureSerializer, PropertySerializer, AgentPropertyOnRequestSerializers, PropertyAdminUpdateSerializer, ReportSerializer, NearestPropertySerializer, PropertyListSerializer, StatusUpdateSerializer
from .models import Draft, Feature, PropertyType, Property, Report
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from django.db.models import Q
from .filters import IsBedroomRangeBackend, IsPriceRangeBackend, PropertyFilter
# Create your views here.


class PropertyTypeApiViewSet(CreateAPIView):
    """Only adminuser can add Property type"""
    permission_classes = [IsAdminUser, ]
    serializer_class = PropertyTypeSerializer
    queryset = PropertyType


class FeatureApiViewSet(CreateAPIView):
    """Only adminuser can add Feature"""
    permission_classes = [IsAdminUser, ]
    serializer_class = FeatureSerializer
    queryset = Feature


class PropertyTypeUpdateApiViewSet(RetrieveUpdateDestroyAPIView):
    """Only adminuser can make changes or delete Property type"""
    permission_classes = [IsAdminUser, ]
    lookup_field = 'id'
    serializer_class = PropertyTypeSerializer
    queryset = PropertyType


class FeatureUpdateApiViewSet(RetrieveUpdateDestroyAPIView):
    """Only adminuser can make changes or delete Feature"""
    permission_classes = [IsAdminUser, ]
    lookup_field = 'id'
    serializer_class = FeatureSerializer
    queryset = Feature


class AddPropertyApiViewSet(CreateAPIView):
    """ Only agent and Admin users can add property"""
    permission_classes = [IsAgentOrDeveloperOrAdmin, ]
    authentication_classes = (TokenAuthentication,)
    parser_classes = [MultiPartParser, FormParser, ]
    serializer_class = PropertySerializer

    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []

        return super().get_parsers()


class PropertyUpdateViewSet(RetrieveUpdateDestroyAPIView):

    'retrieving property based on the property id, Only Admin user Allowed'
    serializer_class = PropertyAdminUpdateSerializer
    permission_classes = [IsAdminUser, ]
    queryset = Property
    lookup_field = 'id'
    lookup_url_kwarg = 'property_id'


class AgentPropertyList(ListAPIView):
    """ List properties owned by an Agent query by id. Allow Any Permission"""
    serializer_class = PropertyListSerializer
    permission_classes = [AllowAny, ]

    def get(self, request, user_id, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def get_queryset(self):
        qs = Property.active_objects.filter(status='published', agent=self.kwargs['user_id'], available=True)
        return qs
   


class PropertyListBaseOnTown(ListAPIView):
    """ List properties Based on town   """
    serializer_class = PropertyListSerializer
    permission_classes = [AllowAny, ]

    def get(self, request, town, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        qs = Property.active_objects.filter(status='published', available=True,
            city=self.kwargs['town'])
        return qs


class PropertyTypeListView(ListAPIView):
    """ List properties Type"""
    serializer_class = PropertyTypeSerializer
    permission_classes = [AllowAny, ]
    queryset = PropertyType.objects.all()


class PropertyFeatureListView(ListAPIView):
    """ List properties Feature"""
    serializer_class = FeatureSerializer
    permission_classes = [AllowAny, ]
    queryset = Feature.objects.all()


class AllPropertiesApiViewSet(ListAPIView):
    """ get all properties AllowAny Permission """
    serializer_class = PropertyListSerializer
    permission_classes = [AllowAny, ]
    filterset_class = PropertyFilter
    queryset = Property.active_objects.all()
    filter_backends = [DistanceToPointFilter,
                       DjangoFilterBackend, IsBedroomRangeBackend, IsPriceRangeBackend, filters.OrderingFilter]
    distance_filter_field = 'location'
    ordering_fields = ['created_at', 'price', 'bedroom']
    # filterset_fields = ['purpose', 'property_type__title', 'bedroom','price', 'keyword']
    def get_queryset(self):
        qs = Property.active_objects.filter(status='published', available = True)
        return qs
# class AllPropertiesApiViewSet(ListAPIView):
#     """ get all properties AllowAny Permission """
#     serializer_class = PropertyListSerializer
#     permission_classes = [AllowAny, ]
#     filterset_class = PropertyFilter
#     # queryset = Property.active_objects.all()
#     filter_backends = [DistanceToPointFilter,
#                        DjangoFilterBackend, IsBedroomRangeBackend, IsPriceRangeBackend, filters.OrderingFilter]
#     distance_filter_field = 'location'
#     ordering_fields = ['created_at', 'price', 'bedroom']
#     filterset_fields = ['purpose', 'property_type__title', 'bedroom','price', 'keyword']
#     def get_queryset(self):
#         queryset = Property.objects.all()
#         miniprice = self.request.query_params.get('miniprice', 0)
#         maxprice = self.request.query_params.get('maxprice', 1000000000000000)
#         minibedroom = self.request.query_params.get('minibedroom', 0)
#         maxbedroom= self.request.query_params.get('maxbedroom', 50)
#         minibathroom= self.request.query_params.get('minibathroom', 0)
#         maxbathroom = self.request.query_params.get('maxbathroom', 50)
#         maxparlour = self.request.query_params.get('maxparlour', 50)
#         miniparlour = self.request.query_params.get('miniparlour', 0)
#         minitoilet = self.request.query_params.get('minitoilet', 0)
#         maxtoilet = self.request.query_params.get('maxtoilet',50)
#         minikitchen = self.request.query_params.get('minikitchen', 0)
#         maxkitchen = self.request.query_params.get('maxkitchen', 50)
#         property_type = self.request.query_params.get('type', 'default')


#         # queryset = queryset.filter(
#         #                             Q(bedroom__gte=maxbedroom),
#         #                             Q(bedroom__lte=minibedroom))

#         queryset = queryset.filter(bedroom__gte=minibedroom,
#                                        bedroom__lte=maxbedroom,
#                                        price__gte=miniprice,
#                                        price__lte = maxprice,
#                                        bathroom__gte=minibathroom,
#                                        bathroom__lte=maxbathroom,
#                                        parlour__gte=miniparlour,
#                                        parlour__lte=maxparlour,
#                                        toilet__gte=minitoilet,
#                                        toilet__lte=maxtoilet,
#                                        kitchen__gte=minikitchen,
#                                        kitchen__lte=maxkitchen,
#                                        property_type__slug = property_type)
#         try:
#             queryset[0]
#             print('redirect to another type of query')
#         except IndexError:
#                 print("redirect")
#         return queryset


class PropertyDetailsReadOnlyApiViewSet(RetrieveAPIView):
    """
    viewing Property instances.
    """
    lookup_field = 'id'
    serializer_class = PropertyListSerializer
    queryset = Property.objects.all()

    # def retrieve(self, request, *args, **kwargs):
    #     obj = self.get_object()
    #     obj.views = obj.views + 1
    #     obj.save(update_fields=("view", ))
    #     return super().retrieve(request, *args, **kwargs)


class PropertyListOnResquestApiViewSet(ListAPIView):
    """ the list of property owned by the current authenticated user"""
    serializer_class = AgentPropertyOnRequestSerializers
    permission_classes = [IsAgentOrDeveloperOrAdmin, ]

    def get_queryset(self):
        id = self.request.user.id
        return Property.active_objects.filter(agent=id)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def flag_property(request, property_id):
    """Only Admin user can flag property"""
    property = get_object_or_404(Property, pk=property_id)
    property.active = False
    property.status = "flagged"
    property.save()
    return Response({"message": f"{property.title} flagged successfully"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAgentOrDeveloperOrAdmin, ])
def unpublish_property(request, property_id):
    """Admin and agent user can unpublish property"""
    property = get_object_or_404(Property, pk=property_id)
    property.active = False
    property.status = "pending"
    property.save()
    return Response({"message": f"{property.title} Unpublished successfully"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([
    IsAgentOrDeveloperOrAdmin])
def property_sold(request, property_id):
    """Admin and agent user can sold property"""
    property = get_object_or_404(Property, pk=property_id)
    property.active = False
    property.status = "sold"
    property.save()
    return Response({"message": f"{property.title} Sold out successfully"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([
    IsAgentOrDeveloperOrAdmin])
def property_availability(request, property_id):
    """Admin and agent user can sold property"""
    property = get_object_or_404(Property, pk=property_id)
    if property.available:
        property.available = False
    else:
        property.available = True
    property.save()
    return Response({"message": f"{property.title} availabilty is {property.available}"},
                    status=status.HTTP_200_OK)


class NearestPropertyToLocation(RetrieveAPIView):
    serializer_class = NearestPropertySerializer
    permission_class = []

    def get(self, request, lat, long, **kwargs):
        data = {"latitude": float(lat), "longitude": float(long)}
        serializer = NearestPropertySerializer(data=data)

        if serializer.is_valid():
            longitude = serializer.validated_data['longitude']
            latitude = serializer.validated_data['latitude']
            user_location1 = (float(lat),
                              float(long))
            user_location = Point(
                float(longitude), float(latitude), srid=4326)
            nearest_five_facilities = Property.active_objects.annotate(
                distance=Distance('location', user_location)).order_by('distance')[:5]
            active_property = Property.active_objects.all()
            """
            to compute the distance between user location and the nearest property location
            """

            # for locations in active_property:
            #     distance = geopy_distance(user_location1, locations.location)
            """
            to search for property within a specified radius"""
            # nearest_five_facilities1 =Property.active_objects.filter(location__distance_lte=(user_location, DistanceMeasure(km=3)))
            # for location in nearest_five_facilities1:
            #     distance = geopy_distance(user_location1, location.location)
            serializer = PropertyListSerializer(
                nearest_five_facilities, many=True)
            # data = json.loads(serialize('json', nearest_five_facilities))
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('invalid input')


class SearchPropertyUsingGeoDataViewset(RetrieveAPIView):
    serializer_class = NearestPropertySerializer
    permission_class = []
    queryset = Property.active_objects.all()

    def get(self, request, lat, long,purpose, **kwargs):
        data = {"longitude": float(long), "latitude": float(lat)}
        serializer = NearestPropertySerializer(data=data)
        

        if serializer.is_valid():
            longitude = serializer.validated_data['longitude']
            latitude = serializer.validated_data['latitude']
            user_location1 = (float(lat),
                              float(long))
            user_location = Point(
                float(longitude), float(latitude), srid=4326)

            """
            to compute the distance between user location and the nearest property location
            """

            # for locations in active_property:
            #     distance = geopy_distance(user_location1, locations.location)
            """
            to search for property within a specified radius"""
            nearest_facilities = Property.active_objects.filter(
                location__distance_lte=(user_location, DistanceMeasure(km=8)), purpose=purpose)
            serializer = PropertyListSerializer(
                nearest_facilities, many=True)
            data = json.loads(serialize('json', nearest_facilities))
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('invalid input')


class SearchPropertyInProminientCityViewset(RetrieveAPIView):
    serializer_class = NearestPropertySerializer
    permission_class = []
    queryset = Property.active_objects.all()

    def get(self, request, lat, long, **kwargs):
        data = {"longitude": float(long), "latitude": float(lat)}
        serializer = NearestPropertySerializer(data=data)

        if serializer.is_valid():
            longitude = serializer.validated_data['longitude']
            latitude = serializer.validated_data['latitude']
            user_location1 = (float(lat),
                              float(long))
            user_location = Point(
                float(longitude), float(latitude), srid=4326)

            """
            to compute the distance between user location and the nearest property location
            """

            # for locations in active_property:
            #     distance = geopy_distance(user_location1, locations.location)
            """
            to search for property within a specified radius"""
            nearest_facilities = Property.active_objects.filter(
                location__distance_lte=(user_location, DistanceMeasure(km=3)))
            serializer = PropertyListSerializer(
                nearest_facilities, many=True)
            data = json.loads(serialize('json', nearest_facilities))
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('invalid input')


@api_view(['GET'])
@permission_classes([
    AllowAny])
def distance_nearest_property(request, lat, long, **kwargs):
    data = {"latitude": float(lat), "longitude": float(long)}
    serializer = NearestPropertySerializer(data=data)
    if serializer.is_valid():
        longitude = serializer.validated_data['longitude']
        latitude = serializer.validated_data['latitude']
        user_location = Point(float(latitude),
                              float(longitude), srid=4326)
        nearest_five_facilities = Property.active_objects.annotate(
            distance=Distance('location', user_location)).order_by('distance')[:5]
        """
        to compute the distance between user location and the nearest property location
        """
        all_distance = []
        for locations in nearest_five_facilities:
            distance = geopy_distance(user_location, locations.location)
            all_distance.append(str(distance))
        return Response({'all_distance': all_distance}, status=status.HTTP_200_OK)
    else:
        return Response('invalid input')


class CreateReportApiViewSet(CreateAPIView):
    """Buyers can report property"""
    serializer_class = ReportSerializer
    permission_classes = [IsBuyer, ]
    queryset = Report


class ReportListApiViewSet(ListAPIView):
    """ All report irrespective of property"""
    serializer_class = ReportSerializer
    permission_class = [IsAdminUser, ]
    queryset = Report.objects.all()


class ReportsPerPropertyApiViewSet(ListAPIView, RetrieveAPIView):
    """get All report Per Property"""
    serializer_class = ReportSerializer
    permission_class = [IsAdminUser, ]
    lookup_field = 'property'
    lookup_url_kwarg = 'property_id'

    def get_queryset(self):
        qs = Report.objects.filter(property=self.kwargs['property_id'])
        return qs


class RetrieveReportApiViewSet(RetrieveDestroyAPIView):
    """Only Admin can retrieve reports"""
    serializer_class = ReportSerializer
    permission_class = [IsAdminUser, ]
    queryset = Report
    lookup_field = 'id'
    lookup_url_kwarg = 'report_id'


@api_view(['GET'])
@permission_classes([IsAdminUser])
def property_count(request):
    "Get count of all, rent and sale property"
    if request.method == 'GET':
        property_count = Property.active_objects.count()
        property_sale_count = Property.active_objects.filter(
            purpose="sale").count()
        property_rent_count = Property.active_objects.filter(
            purpose="rent").count()
        data = {
            "all_property": property_count,
            "property_for_sale": property_sale_count,
            "property_for_rent": property_rent_count
        }
        return Response(data)


class StatusUpdateApiViewSet(RetrieveUpdateAPIView):
    permission_classes = [IsAgentOrDeveloper, ]
    serializer_class = StatusUpdateSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'property_id'

    def get_queryset(self):
        qs = Property.objects.filter(agent_id=self.request.user.id)
        return qs


class CreateDraftApiViewSet(CreateAPIView):
    """
    agent or developer can save incompleted form in draft box 
    """
    serializer_class = CreateDraftSerializer
    permission_classes = (IsAgentOrDeveloper,)
    queryset = Draft


class AllAgentDraftViewSet(ListAPIView):
    """
    list of all draft a logined agent has
    """
    serializer_class = DraftSerializer
    permission_classes = (IsAgentOrDeveloper,)

    def get_queryset(self):
        qs = Draft.objects.filter(user=self.request.user)
        return qs


class DraftUpdateviewSet(RetrieveUpdateDestroyAPIView):
    serializer_class = DraftSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'draft_id'
    permission_classes = (IsAgentOrDeveloper,)

    def get_queryset(self):
        qs = Draft.objects.filter(user=self.request.user)
        return qs


@api_view(['GET']) 
def stateAPI(request, state):
    """
    pass 'state' as route param to get all the states in 🇳🇬 , 
    to get the LGA within a state, instead of state, specify a valid state name"""
    with open("state.json", "r") as read_file:
        data = json.load(read_file)
    if state == 'state':
        return Response(data[0].keys(), status=status.HTTP_200_OK)
    else:
        
        state = state.title()
        try:
            if state == "Fct":
                state = "FCT"
            print("this is abuja", state)
            result = data[0][state]
            return Response(result, status=status.HTTP_200_OK)
        except KeyError:
            return Response('state not found', status=status.HTTP_404_NOT_FOUND)
