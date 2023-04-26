from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('<str:username>/index/', views.index, name='index'),
    #path('send_message/<str:recipient_username>/', views.send_message, name='send_message'),
    path('view_messages/<str:recipient_username>/', views.view_messages, name='view_messages'),

    #path('create_message/', views.create_message, name='create_message'),
    #path('create_message/<str:owner_username>/', views.create_message, name='create_message_with_username'),

    path('received_messages/', views.received_messages, name='received_messages'),
    path('message_sent/<str:owner_username>/', views.message_sent, name='message_sent'),

    path('sent_messages/', views.sent_messages, name='sent_messages'),
    path('<str:owner_username>/create_and_send_message/', views.create_and_send_message, name='create_and_send_message'),

]
