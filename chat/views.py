from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Message
from .serializers import MessageSerializer, UserSerializer

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

# Message View
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

