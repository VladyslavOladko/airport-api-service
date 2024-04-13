from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from airport_service.models import (
    AirplaneType,
    Crew,
    Airport,
    Route,
    Airplane,
    Flight,
    Order, Ticket
)


class AirplaneTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class CrewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "image")


class CrewListSerializer(CrewSerializer):

    class Meta:
        model = Crew
        fields = ("id", "full_name", "image")


class AirportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airport
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(RouteSerializer):
    source = AirportSerializer(read_only=True, many=False)
    destination = AirportSerializer(read_only=True, many=False)


class AirplaneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
        )


class AirplaneListSerializer(AirplaneSerializer):
    airplane = serializers.SlugRelatedField(
        read_only=True,
        many=False,
        slug_field="name"
    )
    all_seats = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "airplane",
            "all_seats",
            "outside_image",
            "inside_image",
        )


class AirplaneDetailSerializer(AirplaneListSerializer):

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "airplane",
            "rows",
            "seats_in_row",
            "all_seats",
            "outside_image",
            "inside_image",
        )


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
            )


class FlightListSerializer(FlightSerializer):
    arrival_place = serializers.CharField(
        read_only=True,
        source="route.source"
    )
    destination_place = serializers.CharField(
        read_only=True,
        source="route.destination"
    )
    seats_available = serializers.IntegerField(read_only=True)

    airplane = AirplaneDetailSerializer(read_only=True)
    crew = CrewListSerializer(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "arrival_place",
            "destination_place",
            "airplane",
            "seats_available",
            "departure_time",
            "arrival_time",
            "crew",
        )


class FlightTicketSerializer(FlightListSerializer):

    class Meta:
        model = Flight
        fields = (
            "id",
            "arrival_place",
            "destination_place",
            "departure_time",
            "arrival_time",
        )


class TicketSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["flight"].airplane,
            ValidationError,
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")
        validators = [
            UniqueTogetherValidator(
                queryset=Ticket.objects.all(), fields=["seat", "row", "flight"]
            )
        ]


class TicketListSerializer(TicketSerializer):

    flight = FlightTicketSerializer(many=False, read_only=True)


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class FlightDetailSerializer(FlightListSerializer):

    taken_seats = TicketSeatsSerializer(
        source="tickets",
        many=True,
        read_only=True
    )
    route = RouteListSerializer(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "seats_available",
            "taken_seats",
            "departure_time",
            "arrival_time",
            "crew",
        )


class TicketDetailSerializer(TicketSerializer):

    flight = FlightDetailSerializer(many=False)


class OrderSerializer(serializers.ModelSerializer):

    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):

    tickets = TicketListSerializer(many=True, read_only=True)


class OrderDetailSerializer(OrderSerializer):

    tickets = TicketDetailSerializer(many=True, read_only=True)
