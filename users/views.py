# django imports
from django.contrib.auth import login

# rest_framework imports
from rest_framework import status, generics, permissions

# knox imports
from knox.views import LoginView as KnoxLoginView

# local app imports
from .serializers import CustomUserSerializer, AuthSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer


class LoginView(KnoxLoginView):
    # login view extending KnoxLoginView
    serializer_class = AuthSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user
