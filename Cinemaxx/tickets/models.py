from django.db import models
from django.contrib.auth import get_user_model
from movies.models import Movie

User = get_user_model()


class Hall(models.Model):
    name = models.CharField(max_length=50)
    rows = models.PositiveIntegerField()
    seats_per_row = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Seat(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    row = models.PositiveIntegerField()
    number = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=1500)

    class Meta:
        unique_together = ('hall', 'row', 'number')

    def __str__(self):
        return f"Row {self.row}, Seat {self.number} - {self.price} ₸"


class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    start_time = models.DateTimeField()

    def __str__(self):
        return f"{self.movie.title} — {self.start_time.strftime('%d/%m/%Y %H:%M')}"
    
    class Meta:
        ordering = ['start_time']
        unique_together = ('movie', 'hall', 'start_time')


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id}"


class Ticket(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('booking', 'seat')

    def __str__(self):
        return f"{self.seat}"
