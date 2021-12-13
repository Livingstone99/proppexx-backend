from property.models import Property
from rest_framework import filters
import django_filters as filter


class IsBedroomRangeBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    min_bedroom = 'min-bedroom'
    max_bedroom = 'max-bedroom'

    def filter_queryset(self, request, queryset, view):
        min_bedroom_value = request.query_params.get(self.min_bedroom, 10)
        max_bedroom_value = request.query_params.get(self.max_bedroom, 0)
        return queryset.filter(bedroom__lte=min_bedroom_value, bedroom__gte=max_bedroom_value)


class IsPriceRangeBackend(filters.BaseFilterBackend):
    """
    Filter that get the minimum and maximum Price.
    """
    min_price = 'min-price'
    max_price = 'max-price'

    def filter_queryset(self, request, queryset, view):
        min_price_value = request.query_params.get(self.min_price, 500000000)
        max_price_value = request.query_params.get(self.max_price, 0)
        return queryset.filter(price__lte=min_price_value, price__gte=max_price_value)
    
class PropertyFilter(filter.FilterSet):
    keyword = filter.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Property
        fields = ['purpose', 'property_type__title', 'bedroom','bathroom', 'kitchen', 'toilet', 'parlour','price', 'keyword']