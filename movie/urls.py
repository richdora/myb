from django.urls import path
from . import views

app_name = 'movie'

urlpatterns = [
    path('create/', views.create_movie, name='create_movie'),
    path('update/<int:movie_id>/', views.update_movie, name='update_movie'),

    path('list/', views.list_movies, name='list_movies'),
    path('list/tag/<str:tag_name>/', views.list_movies, name='list_movies_by_tag'),

    path('delete/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    # Add this new url pattern
]
