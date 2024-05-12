from django.db.models import F, Count

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication

from airport_service.filters import AirportFilter, FlightFilter
from airport_service.models import (
    AirplaneType,
    Crew,
    Airport,
    Route,
    Airplane,
    Flight,
    Order,
)
from airport_service.permissions import IsAdminOrIfAuthenticatedReadOnly

from airport_service.serializers import (
    AirplaneTypeSerializer,
    CrewSerializer,
    AirportSerializer,
    RouteSerializer,
    AirplaneSerializer,
    FlightSerializer,
    OrderSerializer,
    RouteListSerializer,
    AirplaneListSerializer,
    AirplaneDetailSerializer,
    FlightListSerializer,
    CrewListSerializer,
    FlightDetailSerializer,
    OrderListSerializer,
    OrderDetailSerializer,
)


class AirplaneTypeViewSet(viewsets.ModelViewSet):

    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly, )
    authentication_classes = (JWTAuthentication,)


class CrewViewSet(viewsets.ModelViewSet):

    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    authentication_classes = (JWTAuthentication,)

    def get_serializer_class(self):

        if self.action == "list":
            return CrewListSerializer

        return CrewSerializer


class AirportViewSet(viewsets.ModelViewSet):

    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = AirportFilter
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    authentication_classes = (JWTAuthentication,)


class RouteViewSet(viewsets.ModelViewSet):

    queryset = Route.objects.all().select_related("source", "destination")
    serializer_class = RouteSerializer
    authentication_classes = (JWTAuthentication,)

    def get_serializer_class(self):

        if self.action == "list":
            return RouteListSerializer

        return RouteSerializer


class AirplaneViewSet(viewsets.ModelViewSet):

    queryset = Airplane.objects.all().select_related("airplane")
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    authentication_classes = (JWTAuthentication,)

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer

        if self.action == "retrieve":
            return AirplaneDetailSerializer

        return AirplaneSerializer


class FlightViewSet(viewsets.ModelViewSet):

    queryset = (
        Flight.objects.all()
        .select_related(
            "route__source",
            "route__destination",
            "airplane__airplane",
            "crew",
        )
        .annotate(
            seats_available=(
                F("airplane__rows") * F("airplane__seats_in_row")
                - Count("tickets")
            )
        )
    )
    serializer_class = FlightSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = FlightFilter
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):

        route_id_str = self.request.query_params.get("route")
        queryset = self.queryset

        if route_id_str:
            queryset = queryset.filter(route_id=int(route_id_str))

        return queryset

    def get_serializer_class(self):

        if self.action == "list":
            return FlightListSerializer

        if self.action == "retrieve":
            return FlightDetailSerializer

        return FlightSerializer


class OrderPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


class OrderViewSet(viewsets.ModelViewSet):

    queryset = (
        Order.objects.all()
        .prefetch_related(
            "tickets__flight__route__source",
        )
    )
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):

        if self.action == "list":
            return OrderListSerializer

        if self.action == "retrieve":
            return OrderDetailSerializer

        return OrderSerializer
