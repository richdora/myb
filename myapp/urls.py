from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    #path('<str:username>/index/', views.index, name='index'),
    path('view_messages/<str:recipient_username>/', views.view_messages, name='view_messages'),


    path('<str:username>/home/', views.home, name='home'),


    path('received_messages/', views.received_messages, name='received_messages'),
    path('message_sent/<str:owner_username>/', views.message_sent, name='message_sent'),

    path('sent_messages/', views.sent_messages, name='sent_messages'),
    path('<str:owner_username>/create_and_send_message/', views.create_and_send_message, name='create_and_send_message'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path("search/", views.user_search, name="user_search"),

]
