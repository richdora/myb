from django.shortcuts import render, redirect
from .models import Movie, Tag
from .forms import MovieForm
from django.contrib.auth.decorators import login_required
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
import requests
import re
from myapp.models import CustomUser
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

def extract_video_id(url):
    video_id_pattern = re.compile(r'(?:https?:\/\/)?(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)')
    match = video_id_pattern.search(url)

    if match:
        return match.group(1)
    else:
        return None


from django.contrib import messages

@login_required
def create_movie(request, username):
    all_tags = Tag.objects.all().values_list('name', flat=True)
    tags_json = json.dumps(list(all_tags))
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            youtube_link = form.cleaned_data['youtube_link']
            video_id = None
            if "v=" in youtube_link:
                video_id = youtube_link.split('v=')[1].split('&')[0]
            elif "youtu.be/" in youtube_link:
                video_id = youtube_link.split('youtu.be/')[1]

            if not video_id:
                messages.error(request, 'Invalid YouTube link. Please provide a valid link.')
                return render(request, 'movie/create_movie.html', {'form': form})

            title, thumbnail_url = get_video_title(settings.YOUTUBE_API_KEY, video_id)

            if title is None or thumbnail_url is None:
                messages.error(request,
                               'Failed to fetch video details. Please try again with a different YouTube link.')
            else:
                movie = form.save(commit=False)
                movie.owner = request.user  # Assign the user field to the current user
                movie.title = title
                movie.thumbnail_url = thumbnail_url
                movie.save()

                # Add this line to assign the tags to the movie instance
                tags = form.cleaned_data['tags']
                tag_objects = []
                for tag in tags:
                    tag_obj, created = Tag.objects.get_or_create(name=tag.name)
                    tag_objects.append(tag_obj)

                movie.tags.set(tag_objects)
                movie.save()
                """
                    messages.success(request, f"Tags: {tags}")
                    messages.success(request, f"Tag objects: {tag_objects}")
                    messages.success(request, f"Movie Tags: {movie.tags.all()}")
                """
                return redirect('movie:list_movies', username=username)  # Redirect to the list view after saving

    else:
        form = MovieForm()

    return render(request, 'movie/create_movie.html', {'form': form, 'all_tags': all_tags, 'tags_json': tags_json, })


def list_movies(request, username, tag_name=None):
    owner = CustomUser.objects.get(username=username)
    movies = Movie.objects.filter(owner=owner).order_by('-created_at')
    api_key = 'AIzaSyAgQOLRQYizg-LK_0hmWJa5nLfE18wZD3o'

    all_tags = Tag.objects.filter(movie__owner=owner).distinct()

    if tag_name:
        selected_tag = get_object_or_404(Tag, name=tag_name)
        movies = Movie.objects.filter(owner=owner, tags=selected_tag).order_by('-created_at')
    else:
        selected_tag = None
        movies = Movie.objects.filter(owner=owner).order_by('-created_at')



    # Create a Paginator object
    paginator = Paginator(movies, 5)  # Show 5 movies per page
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        movies = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        movies = paginator.page(paginator.num_pages)


    for movie in movies:
        video_id = extract_video_id(movie.youtube_link)
        title, thumbnail_url = get_video_title(api_key, video_id)
        movie.title = title
        if thumbnail_url:
            movie.thumbnail_url = thumbnail_url.replace("default.jpg", "maxresdefault.jpg")


    context = {
        'movies': movies,
        'owner': owner,
        'all_tags': all_tags,
        'selected_tag': selected_tag
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


def list_movies_by_tag(request, username, tag_name):
    owner = CustomUser.objects.get(username=username)
    tag = get_object_or_404(Tag, name=tag_name)
    movies = Movie.objects.filter(owner=owner, tags=tag).order_by('-created_at')

    api_key = 'AIzaSyAgQOLRQYizg-LK_0hmWJa5nLfE18wZD3o'

    for movie in movies:
        video_id = extract_video_id(movie.youtube_link)
        title, thumbnail_url = get_video_title(api_key, video_id)
        movie.title = title
        if thumbnail_url:
            movie.thumbnail_url = thumbnail_url.replace("default.jpg", "maxresdefault.jpg")

    all_tags = Tag.objects.filter(movie__owner=owner).distinct()

    context = {
        'movies': movies,
        'owner': owner,
        'tag_name': tag_name,
        'all_tags': all_tags,
    }
    return render(request, 'movie/list_movies.html', context)


from django.shortcuts import get_object_or_404


@login_required
def update_movie(request, username, movie_id):
    all_tags = Tag.objects.all().values_list('name', flat=True)
    movie = get_object_or_404(Movie, id=movie_id)

    # Check if the logged in user is the owner of the movie
    if request.user != movie.owner:
        messages.error(request, "You are not authorized to update this movie.")
        return redirect('movie:list_movies', username=username)

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            movie = form.save()

            # Clear all tags and re-assign
            movie.tags.clear()
            tags = form.cleaned_data['tags']
            tag_objects = []
            for tag in tags:
                tag_obj, created = Tag.objects.get_or_create(name=tag.name)
                tag_objects.append(tag_obj)

            movie.tags.set(tag_objects)
            movie.save()

            messages.success(request, 'Movie updated successfully')
            return redirect('movie:list_movies', username=username)
    else:
        form = MovieForm(instance=movie)


    tags = list(movie.tags.values_list('name', flat=True))
    tags_json = json.dumps(tags)
    return render(request, 'movie/update_movie.html',
                  {'form': form, 'movie': movie, 'all_tags': all_tags, 'tags_json': tags_json,  'tags': ",".join(tags)})
