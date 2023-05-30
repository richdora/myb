from django.urls import path
from . import views

app_name = 'now'


urlpatterns = [
    path('now/', views.now_list, name='now-list'),
    # Other paths...
]
