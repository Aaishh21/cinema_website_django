import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Showtime, Booking, Ticket, Seat


def payment(request):
    return render(request, 'tickets/payment.html')


def place(request):
    showtime_id = request.GET.get('showtime_id')
    showtime = None
    booked_seats = []
    hall_seats = []
    
    if showtime_id:
        showtime = get_object_or_404(Showtime, id=showtime_id)
        
        booked_seat_ids = Ticket.objects.filter(
            booking__showtime=showtime
        ).values_list('seat__id', flat=True)
        booked_seats = list(booked_seat_ids)
        
        seats = Seat.objects.filter(hall=showtime.hall).values(
            'id', 'row', 'number', 'price'
        ).order_by('row', 'number')
        
        hall_seats = [
            {
                'id': seat['id'],
                'row': seat['row'],
                'number': seat['number'],
                'price': float(seat['price'])
            }
            for seat in seats
        ]
    
    return render(request, 'tickets/place.html', {
        'showtime': showtime,
        'booked_seats': booked_seats,
        'hall_seats': hall_seats
    })


@login_required(login_url='users:login')
def create_booking(request):
    if request.method == "POST":
        showtime_id = request.POST.get('showtime_id')
        seats_json = request.POST.get('seats', '[]')
        
        showtime = get_object_or_404(Showtime, id=showtime_id)
        seat_ids = json.loads(seats_json)
        
        if not seat_ids:
            return redirect('tickets:place')
        
        booking = Booking.objects.create(
            user=request.user,
            showtime=showtime
        )
        
        for seat_id in seat_ids:
            seat = get_object_or_404(Seat, id=seat_id)
            Ticket.objects.create(
                booking=booking,
                seat=seat
            )
        
        return redirect('tickets:ticket-success', booking_id=booking.id)
    
    return redirect('tickets:place')


def cancel_booking(request):
    """Redirect back to movie detail page"""
    showtime_id = request.GET.get('showtime_id')
    
    if showtime_id:
        try:
            showtime = get_object_or_404(Showtime, id=showtime_id)
            return redirect('movies:movie', movie_id=showtime.movie.id)
        except:
            pass
    
    return redirect('movies:homepage')


@login_required(login_url='users:login')
def ticket_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    tickets = Ticket.objects.filter(booking=booking).select_related('seat')
    
    tickets_data = [
        {
            'seat': {
                'row': ticket.seat.row,
                'number': ticket.seat.number,
                'price': float(ticket.seat.price)
            }
        }
        for ticket in tickets
    ]
    
    context = {
        'booking': booking,
        'tickets': tickets,
        'tickets_json': json.dumps(tickets_data)
    }
    
    return render(request, 'tickets/ticket_success.html', context)


@login_required(login_url='users:login')
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "tickets/booking_history.html", {
        "bookings": bookings
    })