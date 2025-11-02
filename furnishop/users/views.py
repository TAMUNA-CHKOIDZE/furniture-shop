from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login, logout
from users.models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, ChangePasswordSerializer


# Register
# CreateAPIView = POST ფუნქციონალი
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    # RegisterSerializer ახალი მომხმარებლის რეგისტრაციისთვის
    serializer_class = RegisterSerializer
    # AllowAny ნიშნავს, რომ რეგისტრაცია ყველასთვის ხელმისაწვდომია
    permission_classes = [AllowAny]


# Login
# ეს არის session-based login, ანუ cookie-ის მეშვეობით მომხმარებელი დარჩება სისტემაში შესული
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)  # session-based login
        return Response({'detail': 'Logged in successfully'})


# Logout
# Session-ის გასაწმენდი logout.
class LogoutView(generics.GenericAPIView):
    # IsAuthenticated ნიშნავს, რომ მხოლოდ შესული მომხმარებლები შეძლებენ logout-ს.
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'detail': 'Logged out successfully'})


# Profile
class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# Change password
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.object.set_password(serializer.validated_data['new_password'])
        self.object.save()
        return Response({'detail': 'Password updated successfully'})
