from django.urls import path
from . import views


app_name = 'memo'


urlpatterns = [
    path('list/', views.memo_list, name='memo_list'),
    path('tag/<str:tag_name>/', views.memo_list, name='memo_list_by_tag'),

    path('create/', views.memo_create, name='memo_create'),
    path('update/<int:pk>/', views.memo_update, name='memo_update'),
    path('delete/<int:pk>/', views.memo_delete, name='memo_delete'),
    path('view/<int:pk>/', views.memo_view, name='memo_view'),
    path('password/<int:pk>/', views.memo_password, name='memo_password'),

]
