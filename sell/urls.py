from django.urls import path
from . import views

app_name = 'sell'

urlpatterns = [
    path('<str:owner_name>/list/', views.sell_list, name='sell_list'),
    path('<str:owner_name>/create/', views.sell_create, name='sell_create'),
    path('<str:owner_name>/update/<int:pk>/', views.sell_update, name='sell_update'),
    path('<str:owner_name>/delete/<int:pk>/', views.sell_delete, name='sell_delete'),
    # other URL patterns...
]
