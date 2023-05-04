from django.urls import path
from . import views

app_name = 'movie'

urlpatterns = [
    path('create/', views.create_movie, name='create_movie'),
    path('list_movies/', views.list_movies, name='list_movies'),
    path('delete/<int:movie_id>/', views.delete_movie, name='delete_movie'),
]

