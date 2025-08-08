from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from .authentication import CsrfExemptSessionAuthentication
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import UpdateUserSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError


class RegisterView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    
    def get(self, request):
        return Response({"message": "Use the POST to register"})

    
    def post(self, request):
        username = request.data.get("username")
        if User.objects.filter(username=username).exists():
            return Response({"message": "User already exists. Please login"}, status=status.HTTP_302_FOUND)
        
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created."}, status=status.HTTP_201_CREATED)
        else:
            first_error_field = next(iter(serializer.errors))
            first_error_message = serializer.errors[first_error_field][0]
            return Response({"message": first_error_message}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    
    def get(self, request):
        if request.user.is_authenticated:
            return Response({"logged_in_as": request.user.username})
        else:
            return Response({"message": "No user is logged in now"})
    
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user_exists = User.objects.filter(username=username).exists()
        if not user_exists:
            return Response({"message": "User does not exist. Please register"}, status=status.HTTP_404_NOT_FOUND)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    
    def get(self, request):
        if request.user.is_authenticated:
            return Response({"message": f"{request.user.username} is currently logged in."})
        return Response({"message": "No user is logged in."})
    
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


class UpdateUserView(generics.UpdateAPIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdateUserSerializer
    queryset = User.objects.all()

    def get_object(self):       
        return self.request.user

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            raise PermissionDenied(detail="Please login before updating.")
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied(detail="Please log in before updating your profile.")
        response = super().put(request, *args, **kwargs)
        return Response({
            "message": "Updated successfully",
            "data": response.data
        }, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied(detail="Please log in before updating your profile.")
        response = super().patch(request, *args, **kwargs)
        return Response({
            "message": "Updated successfully",
            "data": response.data
        }, status=status.HTTP_200_OK)
        
        

class DeleteUserView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "phone_number":user.phone
        })

    def delete(self, request):
        password = request.data.get("password")
        user = request.user
        
        if not password:
            return Response({"message": "Password is required to delete your account."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({"message": "Incorrect password."}, status=status.HTTP_403_FORBIDDEN)

        user.delete()
        return Response({"message": "Account deleted successfully."}, status=status.HTTP_200_OK)
