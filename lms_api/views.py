from django.shortcuts import render
from .models import Library, LibraryUser
from rest_framework import serializers
from .serializers import LibrarySerializer, AdminSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication, BaseAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.utils.decorators import method_decorator

# Admin View.....

class LibraryView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin, mixins.DestroyModelMixin  ):
    serializer_class = LibrarySerializer
    queryset = Library.objects.all()

    lookup_field = 'id'

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)

# General View.....

class GeneralView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin, mixins.DestroyModelMixin  ):
    serializer_class = LibrarySerializer
    queryset = Library.objects.all()

    lookup_field = 'id'

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)


# Library User Sing Up...

class AdminSignup(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = AdminSerializer
    queryset = LibraryUser.objects.all()

    lookup_field = 'id'

    def post(self, request):
        return self.create(request)

# Library User Sign In...
    
class AdminSignin(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        
        user = authenticate(email=email, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                
                data = {
                    'token': f"Token {Token.objects.get_or_create(user=user)[0].key}"
                }

                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(msg="User is inactive", status=status.HTTP_404_NOT_FOUND)
        return Response("Invalid Username or Password", status=status.HTTP_401_UNAUTHORIZED)

# Library User Logout...

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def user_logout(request):
  request.user.auth_token.delete()
  logout(request)
  return Response("Logged out", status=status.HTTP_200_OK)