from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Movie, Genre, Contact, Feedback, Comment
from tickets.models import Showtime

def homepage(request):
    genres = Genre.objects.all()
    return render(request, 'movies/homepage.html', {'genres': genres})

def movies(request):
    trending_movies = Movie.objects.filter(is_trending=True)
    coming_soon_movies = Movie.objects.filter(is_coming_soon=True)
    hero_movies = Movie.objects.filter(is_hero=True)[:4]
    
    if not hero_movies:
        hero_movies = trending_movies[:4] if trending_movies else Movie.objects.all()[:4]
    
    all_movies = Movie.objects.all()
    
    selected_genre = request.GET.get('genre', '')
    selected_rating = request.GET.get('rating', '')
    
    filtered_movies = all_movies
    
    if selected_genre:
        filtered_movies = filtered_movies.filter(genre__id=selected_genre)
    
    if selected_rating:
        try:
            min_rating = float(selected_rating)
            filtered_movies = filtered_movies.filter(rating__gte=min_rating)
        except ValueError:
            pass
    
    genres = Genre.objects.all()
    
    paginator = Paginator(filtered_movies, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'trending': trending_movies,
        'coming_soon_movies': coming_soon_movies,
        'hero_movies': hero_movies,
        'all_movies': all_movies,
        'filtered_movies': filtered_movies,
        'page_obj': page_obj,
        'genres': genres,
        'selected_genre': selected_genre,
        'selected_rating': selected_rating,
    }
    return render(request, 'movies/movies.html', context)

def specific_genre(request, genre_id): 
    genre = get_object_or_404(Genre, id=genre_id)
    movies = Movie.objects.filter(genre=genre) 
    return render(request, 'movies/specific_genre.html', {'genre': genre, 'movies': movies})

def movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    showtimes = Showtime.objects.filter(movie=movie).order_by('start_time')
    comments = movie.comments.all()
    
    context = {
        'movie': movie, 
        'showtimes': showtimes,
        'comments': comments
    }
    return render(request, 'movies/index.html', context)

def contact(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message')
        
        Contact.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            message=message
        )
        
        return JsonResponse({'success': True, 'message': 'Your message has been sent successfully!'})
    
    return render(request, 'movies/contact.html')


@require_http_methods(["POST"])
def submit_feedback(request):
    name = request.POST.get('name')
    rating = request.POST.get('rating')
    message = request.POST.get('message')
    
    try:
        Feedback.objects.create(
            name=name,
            rating=int(rating),
            message=message
        )
        return JsonResponse({'success': True, 'message': 'Thank you for your feedback!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@login_required(login_url='users:login')
@require_http_methods(["POST"])
def add_comment(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    comment_text = request.POST.get('comment_text', '').strip()
    
    if not comment_text:
        return JsonResponse({'success': False, 'message': 'Comment cannot be empty'}, status=400)
    
    try:
        comment = Comment.objects.create(
            movie=movie,
            user=request.user,
            text=comment_text
        )
        return JsonResponse({
            'success': True, 
            'message': 'Comment added successfully!',
            'comment': {
                'id': comment.id,
                'username': comment.user.username,
                'text': comment.text,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@login_required(login_url='users:login')
@require_http_methods(["POST"])
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.user != request.user:
        return JsonResponse({'success': False, 'message': 'You can only delete your own comments'}, status=403)
    
    try:
        comment.delete()
        return JsonResponse({'success': True, 'message': 'Comment deleted successfully!'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)
