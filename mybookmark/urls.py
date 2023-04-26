from django.urls import path
from . import views

app_name = 'mybookmark'

urlpatterns = [
    path('create/', views.create_bookmark, name='create_bookmark'),
    path('list_bookmarks/', views.list_bookmarks, name='list_bookmarks'),
    path('delete/<int:bookmark_id>/', views.delete_bookmark, name='delete_bookmark'),
]

