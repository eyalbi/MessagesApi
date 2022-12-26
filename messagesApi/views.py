from django.http import JsonResponse
from .models import Message
from django.contrib.auth.models import User
from django.db.models import Q
from .serializers import MessageSerializer,UserSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .utils import staff_required 



@api_view(['GET','POST'])
def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'Message':"success"},status = status.HTTP_200_OK)
        else:
            return JsonResponse({'Message':"user credentials failure"},status = status.HTTP_401_UNAUTHORIZED)
    elif request.method == 'GET':
        return JsonResponse({'Message':"Please Login A user"},status = status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED)


@api_view(['GET'])
def logoutUser(request):
    logout(request)
    return JsonResponse({'Message':'User Logedout' })


@staff_required(login_url="../admin")
@api_view(['GET'])
def getAllUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users,many=True)
    return JsonResponse({'User': serializer.data})


@login_required()
@api_view(['GET'])
def messagesList(request):
    if request.user.is_authenticated:
        messages = Message.objects.filter(Q(sender=request.user.id) | Q(receiver=request.user.id))
    else:
        messages = []
    serializer = MessageSerializer(messages,many=True)
    return JsonResponse({'Message':serializer.data})

@login_required()
@api_view(['GET'])
def readMessage(request):
    if not request.user.is_authenticated:
       return JsonResponse({'Message':'login Required'},status = status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED) 
    message = Message.objects.filter(receiver = request.user.id ,HasBeenRead = False).first()
    if message:
        message.HasBeenRead = True
        message.save()
        serializer = MessageSerializer(message)
        return JsonResponse({'Message':serializer.data})
    return JsonResponse({'Message':"No Messages"})
    

@login_required()
@api_view(['GET'])
def UnreadmessagesList(request):
    messages = Message.objects.filter(Q(HasBeenRead = False) & Q(receiver = request.user.id))
    if messages:
        serializer = MessageSerializer(messages,many=True)
        return JsonResponse({'Message':serializer.data})
    return JsonResponse({'Message':"No New Messages"})


@api_view(['POST'])
def writeMessage(request):
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"Message": "Message created","data":serializer.data}, status=status.HTTP_201_CREATED)
    return JsonResponse({"Message": "Message invalid"},status = status.HTTP_400_BAD_REQUEST)

login_required()
@api_view(['DELETE'])
def deleteMessage(request,id):
    try:
        message = Message.objects.get(pk=id)
    except:
        return JsonResponse({'message':"No such Message"},status=status.HTTP_404_NOT_FOUND)
    if message.receiver.id == request.user.id or message.sender.id == request.user.id:
        messageResponseData = MessageSerializer(message)
        message.delete()
        return JsonResponse({"Message" : "Message Deleted",'data': messageResponseData.data},status=status.HTTP_200_OK)
    return JsonResponse({'Message':"you are not allowed to delete this message"}, status=status.HTTP_403_FORBIDDEN)



 


