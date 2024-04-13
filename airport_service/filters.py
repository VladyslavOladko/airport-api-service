from django_filters import rest_framework as filters

from airport_service.models import Airport, Flight


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class AirportFilter(filters.FilterSet):

    city = CharFilterInFilter(field_name="city", lookup_expr="in")

    class Meta:
        model = Airport
        fields = ("city", )


class FlightFilter(filters.FilterSet):

    arrival_place = CharFilterInFilter(
        field_name="route__source__name",
        lookup_expr="in"
    )
    destination_place = CharFilterInFilter(
        field_name="route__destination__name",
        lookup_expr="in"
    )
    departure_time = filters.DateTimeFromToRangeFilter()
    arrival_time = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Flight
        fields = (
            "arrival_place",
            "destination_place",
            "departure_time",
            "arrival_time"
        )
