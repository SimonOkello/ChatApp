from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Message
from .serializers import MessageSerializer, UserSerializer
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login


# Create your views here.
# User view
@csrf_exempt
def user_list(request, pk=None):
    if request.method=='GET':
        if pk:
            users = User.objects.filter(id=pk)
        else:
            users = User.objects.all()
        serializer = UserSerializer(users, many=True, context = {'request':request})
        return JsonResponse(serializer.data, safe=False)

    elif request.method=='POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

# Message list View
@csrf_exempt
def message_list(request, sender=None, receiver=None):
    if request.method=='GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id = receiver)
        serializer = MessageSerializer(messages, many=True, context={'request':request})
        return JsonResponse(serializer.data, safe=False)
    elif request.method=='POST':
        data =JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

# index view
def index(request):
    if request.user.is_authenticated:
        return redirect('chats')
    if request.method=='GET':
        return render(request, 'index.html', {})
    if request.method == 'POST':
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse('{"error": "User does not exist"}')
        return redirect('chats')

# chats view
def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == 'GET':
        return render(request, 'chat.html', {'users': User.objects.exclude(username=request.user.username)})
    

# register view
def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'register.html', {})

# message view

def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == 'GET':
        return render(request, 'message.html', {
            'users': User.objects.exclude(username = request.user.username),
            'receiver': User.objects.get(id=receiver),
            'messages': Message.objects.filter(sender_id=sender, receiver_id =receiver) |
                        Message.objects.filter(sender_id=receiver, receiver_id=sender)
        })
