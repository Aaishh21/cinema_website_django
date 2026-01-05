from django.urls import path

from movies.views import homepage, movies, specific_genre, movie, contact, submit_feedback, add_comment, delete_comment
app_name = 'movies'

urlpatterns = [
    path('', homepage, name='homepage'),
    path('movies/', movies, name='movies'),
    path('movies/specific-genre/<int:genre_id>/', specific_genre, name='specific_genre'),
    path('movies/index/<int:movie_id>/', movie, name='movie'),
    path('movies/contact/', contact, name='contact'),
    path('movies/submit-feedback/', submit_feedback, name='submit_feedback'),
    path('movies/<int:movie_id>/add-comment/', add_comment, name='add_comment'),
    path('comments/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
]