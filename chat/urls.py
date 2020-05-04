from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import user_list, message_list, index,chat_view, register, message_view

urlpatterns = [
    path('', index, name = 'index' ),
    path('register', register, name = 'register'),
    path('chat/', chat_view, name = 'chats' ),
    path('chat/<int:sender>/<int:receiver>', message_view, name='chat'),
    path('api/messages/<int:sender>/<int:receiver>/', message_list, name='message-detail'),
    path('api/messages/', message_list, name= 'message-list'),
    path('api/users/', user_list, name='users'),
    path('api/users/<int:pk>/', user_list, name='user-detail'),
    path('logout', LogoutView.as_view(next_page = 'index'), name='logout'),
]