from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_app.models import User
from drf_app.serializers import UserSerializer
from rest_framework import status

# Create your views here.


@api_view(['GET'])
def user_list(request):
    """
    List all code User
    """
    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
    

@api_view(['GET','POST'])
def hello_world(request):
    if request.method == 'GET':
        return Response({'msg':'This is GET Request'})
    
    if request.method == "POST":
        print(request.data)
        return Response({'msg':"This IS POST Request",'data':request.data})
    



@api_view(['GET'])
def user_api(request,id=None):
    if request.method =='GET':
        id=request.data.get('id')
        if id is not None:
            user=User.objects.get(id=id)
            serializer=UserSerializer(user)
            return Response(serializer.data)
        users=User.objects.all()
        serializer=UserSerializer(users,many=True)
        return Response(serializer.data)


@api_view(['POST'])
def add_user(request):
    if request.method == 'POST':
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'user add succesfully'})
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['PUT'])
def update_user(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'msg':'user Update Succesfully'},status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_user(request,id):
    if request.method == 'DELETE':
        user=User.objects.get(id=id)
        user.delete()
        return Response({'msg':'user delete Succesfully'},status=status.HTTP_204_NO_CONTENT)