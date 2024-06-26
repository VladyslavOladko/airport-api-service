from django.contrib import admin

from airport_service.models import (
    Ticket,
    Order,
    AirplaneType,
    Crew,
    Airport,
    Route,
    Airplane,
    Flight
)


class TicketInLine(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInLine,)


admin.site.register(AirplaneType)
admin.site.register(Crew)
admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(Airplane)
admin.site.register(Flight)
admin.site.register(Ticket)
