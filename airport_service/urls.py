from rest_framework import routers

from airport_service.views import (
    AirplaneTypeViewSet,
    CrewViewSet,
    AirportViewSet,
    RouteViewSet,
    AirplaneViewSet,
    FlightViewSet,
    OrderViewSet,
)

router = routers.DefaultRouter()

router.register("airplane-types", AirplaneTypeViewSet)
router.register("crew", CrewViewSet)
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("flights", FlightViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [] + router.urls

app_name = "airport_service"
