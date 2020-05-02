from django.urls import path
from .views import user_list, message_list

urlpatterns = [
    path('api/messages/<int:sender>/<int:receiver>/', message_list, name='message-detail'),
    path('api/messages/', message_list, name= 'message-list'),
    path('api/users/', user_list, name='users'),
    path('api/users/<int:pk>/', user_list, name='user-detail'),
]