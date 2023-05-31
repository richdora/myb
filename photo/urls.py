from django.urls import path
from . import views

app_name = 'photo'

urlpatterns = [
    path('list/', views.photo_list, name='photo_list'),
    path('list/tag/<str:tag_name>/', views.photo_list, name='photo_list_by_tag'),
    path('create/', views.photo_create, name='photo_create'),
    path('delete/<int:photo_id>/', views.photo_delete, name='photo_delete'),
    path('photo/<int:photo_id>/update/', views.photo_update, name='photo_update'),
    path('photo/<int:photo_id>/', views.photo_view, name='photo_view'),
]
