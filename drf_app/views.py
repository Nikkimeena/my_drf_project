from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_app.models import User,Book
from drf_app.serializers import UserSerializer,BookSerializer,PersonSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404

# Create your views here.


"""Function Based view"""

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
    

"""get user """

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

""" Create the User"""

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
    
""" Update User """   

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

""" Delete the User"""

@api_view(['DELETE'])
def delete_user(request,id):
    if request.method == 'DELETE':
        user=User.objects.get(id=id)
        user.delete()
        return Response({'msg':'user delete Succesfully'},status=status.HTTP_204_NO_CONTENT)
    

#########################################################################################################################################   

"""Class Based View"""


class UserList(APIView):

    """
    List all users or Create a new User
    """
    def get(self,request,format=None):
        breakpoint()
        users=User.objects.all()

        serializer=UserSerializer(users,many=True)
        return Response(serializer.data)
    
    def post(self,request,format=None):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class UserDetail(APIView):
    """
    Retrieve ,Update or Delete A User Instance
    """
    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
        
    def get(self,request,pk,format=None):
        user=self.get_object(pk)
        serializer=UserSerializer(user)
        return Response(serializer.data)
    
    def put(self,request,pk,format=None):
        user=self.get_object(pk)
        serializer=UserSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user,data=request.data, partial=True)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self,request,pk,format=None):
        user=self.get_object(pk)
        user.delete()
        return Response({'msg':'user delete Succesfully'},status=status.HTTP_204_NO_CONTENT)



#######################################################################################################################################
    """ Mixin View Drf"""   
from rest_framework import mixins
from rest_framework import generics


class AllUserList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset=User.objects.all()
    # breakpoint()
    serializer_class=UserSerializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    

class UserInfo(mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               generics.GenericAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer


    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    
    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)
    
    # def patch(self,request,*args,**kwargs):
    #     return self.update(request,*args,**kwargs)
    
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)
    

############################################################################################################################################
"""Generic View Api"""

from rest_framework import generics


class List(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


####################################################################################################################################
    


"""concrite Api View """

from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView,ListCreateAPIView,RetrieveUpdateAPIView,RetrieveDestroyAPIView,RetrieveUpdateDestroyAPIView


class BookList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookCreate(CreateAPIView):
    books=Book.objects.all()
    serializer_class=BookSerializer


class BookRetreive(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookUpdate(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDelete(DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class=BookSerializer


class BookListCreate(ListCreateAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer


class BookRetrieveUpdate(RetrieveUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class=BookSerializer



class Book_delete(RetrieveDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class=BookSerializer



class Book_update_delete(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class=BookSerializer


############################################################################################################################################3

""" basic Authentication in django"""

from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser



class BookViewset(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes=[IsAdminUser]



class BookReadOnly(viewsets.ReadOnlyModelViewSet):
    queryset=Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes=[BasicAuthentication]
    # permission_classes=[IsAuthenticated]
    # permission_classes =[AllowAny]
    permission_classes=[IsAdminUser]


###########################################################################################################

"""Session Authentoication in django"""


from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
# from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser,IsAuthenticatedOrReadOnly,DjangoModelPermissions,DjangoModelPermissionsOrAnonReadOnly
from .models import Person
from .custompermission import Permission


class PersonViewset(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    # permission_classes=[IsAdminUser]
    # permission_classes=[IsAdminUser]
    # permission_classes=[IsAuthenticatedOrReadOnly]
    # permission_classes=[DjangoModelPermissions]

    # permission_classes=[DjangoModelPermissionsOrAnonReadOnly]
    permission_classes=[Permission]

    


   
