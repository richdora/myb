
from django.urls import path
from . import views

urlpatterns = [
    path('photo/list/', views.photo_list, name='photo_list'),
    path('photo/create/', views.photo_create, name='photo_create'),
    path('photo/delete/<int:photo_id>/', views.photo_delete, name='photo_delete'),
]
