from django.shortcuts import render, redirect
from .models import Movie
from .forms import MovieForm
from django.contrib.auth.decorators import login_required
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
import requests
import re
from myapp.models import CustomUser

def extract_video_id(url):
    video_id_pattern = re.compile(r'(?:https?:\/\/)?(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)')
    match = video_id_pattern.search(url)

    if match:
        return match.group(1)
    else:
        return None



@login_required
def create_movie(request, username):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.owner = request.user  # Assign the user field to the current user
            movie.save()
            return redirect('movie:list_movies', username=username)  # Redirect to the list view after saving
    else:
        form = MovieForm()
    return render(request, 'movie/create_movie.html', {'form': form})


def list_movies(request, username):
    owner = CustomUser.objects.get(username=username)
    movies = Movie.objects.filter(owner=owner).order_by('-created_at')
    api_key = 'AIzaSyAgQOLRQYizg-LK_0hmWJa5nLfE18wZD3o'

    for movie in movies:
        video_id = extract_video_id(movie.youtube_link)
        title, thumbnail_url = get_video_title(api_key, video_id)
        movie.title = title
        movie.thumbnail_url = thumbnail_url.replace("default.jpg", "maxresdefault.jpg")
    context = {
        'movies': movies, 'owner': owner,
    }
    return render(request, 'movie/list_movies.html', context)


def get_video_title(api_key, video_id):
    url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=snippet'
    response = requests.get(url)
    response_json = response.json()

    page_info = response_json.get('pageInfo', {})
    total_results = page_info.get('totalResults', 0)

    if total_results > 0:
        items = response_json.get('items', [{}])
        snippet = items[0].get('snippet', {})
        title = snippet.get('title', 'Unknown Title')
        thumbnails = snippet.get('thumbnails', {})
        default_thumbnail = thumbnails.get('default', {})
        thumbnail_url = default_thumbnail.get('url', None)
        return title, thumbnail_url
    else:
        return 'Unknown Title', None


@login_required
def delete_movie(request, username, movie_id):
    owner = CustomUser.objects.get(username=username)
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.user == owner:
        movie.delete()
        return redirect('movie:list_movies', username=username)
    else:
        return redirect('movie:list_movies', username=username)


