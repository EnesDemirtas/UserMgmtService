# django imports
from django.contrib.auth import login, update_session_auth_hash

# rest_framework imports
from rest_framework import generics, permissions, viewsets, status

# knox imports
from knox.views import LoginView as KnoxLoginView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# local app imports
from .serializers import CustomUserSerializer, AuthSerializer, AuthTokenSerializer, CustomUserAddressSerializer, \
    ChangePasswordSerializer
from .models import CustomUserAddress


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

    def perform_update(self, serializer):
        """Update authenticated user"""
        serializer.save(user=self.request.user)


class CustomUserAddressViewSet(viewsets.ModelViewSet):
    queryset = CustomUserAddress.objects.all()
    serializer_class = CustomUserAddressSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
