from django.urls import path, include
from knox import views as knox_views
from rest_framework.routers import DefaultRouter
from .views import CreateUserView, LoginView, ManageUserView, CustomUserAddressViewSet

router = DefaultRouter()
router.register(r'addresses', CustomUserAddressViewSet)

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('profile/', ManageUserView.as_view(), name='profile'),
    path('login/', LoginView.as_view(), name='knox_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('profile/', include(router.urls))
]
