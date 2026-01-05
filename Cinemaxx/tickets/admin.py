from django.contrib import admin
from .models import Hall, Seat, Showtime, Booking, Ticket


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('name', 'rows', 'seats_per_row', 'total_seats')
    
    def total_seats(self, obj):
        return obj.rows * obj.seats_per_row
    total_seats.short_description = 'Total Seats'


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('id', 'hall', 'row', 'number')
    list_filter = ('hall', 'row')
    search_fields = ('hall__name',)


@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'hall', 'start_time', 'booked_seats')
    list_filter = ('movie', 'hall', 'start_time')
    search_fields = ('movie__title', 'hall__name')
    ordering = ('-start_time',)
    
    def booked_seats(self, obj):
        return Ticket.objects.filter(booking__showtime=obj).count()
    booked_seats.short_description = 'Booked Seats'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'showtime', 'created_at', 'ticket_count')
    list_filter = ('created_at', 'showtime__movie', 'showtime__hall')
    search_fields = ('user__email', 'user__full_name')
    readonly_fields = ('created_at',)
    
    def ticket_count(self, obj):
        return obj.ticket_set.count()
    ticket_count.short_description = 'Tickets'


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'seat', 'showtime')
    list_filter = ('booking__created_at', 'booking__showtime__hall')
    search_fields = ('booking__user__email', 'seat__hall__name')
    
    def showtime(self, obj):
        return obj.booking.showtime
    showtime.short_description = 'Showtime'