from django.contrib import admin
from .models import Movie, Genre, Contact, Feedback, Comment


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'release_date', 'duration', 'rating', 'age_rating', 'is_trending', 'is_coming_soon', 'is_hero', 'is_active')
    list_filter = ('genre', 'release_date', 'is_active', 'is_trending', 'is_coming_soon', 'is_hero')
    search_fields = ('title', 'description', 'directors', 'cast')
    list_editable = ('is_active', 'is_trending', 'is_coming_soon', 'is_hero')
    fieldsets = (
        ('Movie Info', {
            'fields': ('title', 'description', 'genre', 'duration', 'rating', 'age_rating')
        }),
        ('Cast & Crew', {
            'fields': ('directors', 'cast')
        }),
        ('Media', {
            'fields': ('poster', 'horizontal_poster', 'trailer')
        }),
        ('Availability', {
            'fields': ('is_active', 'release_date', 'is_trending', 'is_coming_soon', 'is_hero')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'created_at')
    list_filter = ('movie', 'created_at')
    search_fields = ('user__username', 'movie__title', 'text')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Comment Information', {
            'fields': ('movie', 'user', 'text')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('first_name', 'last_name', 'email', 'message')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Contact Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'message')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Feedback Information', {
            'fields': ('name', 'rating', 'message')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )


