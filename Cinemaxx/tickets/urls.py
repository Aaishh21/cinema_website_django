from django.urls import path

from tickets.views import payment, place, ticket_success, create_booking, cancel_booking
app_name = 'tickets'

urlpatterns = [
    path('payment/', payment, name='payment'),
    path('place/', place, name='place'),
    path('create-booking/', create_booking, name='create-booking'),
    path('cancel-booking/', cancel_booking, name='cancel-booking'),
    path('ticket-success/<int:booking_id>/', ticket_success, name='ticket-success'),
]