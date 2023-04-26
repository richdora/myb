from django.urls import path
from . import views


app_name = 'memo'


urlpatterns = [
    path('<str:owner_name>/list/', views.memo_list, name='memo_list'),
    path('<str:owner_name>/create/', views.memo_create, name='memo_create'),
    path('<str:owner_name>/update/<int:pk>/', views.memo_update, name='memo_update'),
    path('<str:owner_name>/delete/<int:pk>/', views.memo_delete, name='memo_delete'),
    path('<str:owner_name>/view/<int:pk>/', views.memo_view, name='memo_view'),
]
