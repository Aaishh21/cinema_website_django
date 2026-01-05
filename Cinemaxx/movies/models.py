from django.db import models
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True, related_name='movies')
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    directors = models.CharField(max_length=255, blank=True)
    cast = models.TextField(blank=True)
    description = models.TextField()
    poster = models.ImageField(upload_to='movie_posters/', null=True, blank=True)
    horizontal_poster = models.ImageField(upload_to='movie_posters/', null=True, blank=True, help_text="Large horizontal poster for hero/banner sections")
    trailer = models.FileField(upload_to='movie_trailers/', null=True, blank=True)
    rating = models.FloatField(default=0, help_text="Rating out of 10")
    is_active = models.BooleanField(default=True)
    age_rating = models.CharField(max_length=10, default="16+") 
    is_trending = models.BooleanField(default=False) 
    is_coming_soon = models.BooleanField(default=False) 
    is_hero = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-release_date']


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
    
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['-created_at']


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
    
    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ['-created_at']


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.rating}/5 stars"
    
    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"
        ordering = ['-created_at']
