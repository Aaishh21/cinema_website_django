from django.core.management.base import BaseCommand
from tickets.models import Hall, Seat


class Command(BaseCommand):
    help = 'Populate seats for all halls with calculated prices'

    def handle(self, *args, **options):
        halls = Hall.objects.all()
        total_seats_created = 0
        
        for hall in halls:
            Seat.objects.filter(hall=hall).delete()
            
            seats_to_create = []
            base_price = 1500  
            price_increment = 100 
            
            for row in range(1, hall.rows + 1):
                row_price = base_price + (hall.rows - row) * price_increment
                
                for seat_num in range(1, hall.seats_per_row + 1):
                    seats_to_create.append(
                        Seat(hall=hall, row=row, number=seat_num, price=row_price)
                    )
            
            Seat.objects.bulk_create(seats_to_create)
            seats_created = len(seats_to_create)
            total_seats_created += seats_created
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created {seats_created} seats for {hall.name}'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nTotal: {total_seats_created} seats created successfully!'
            )
        )
