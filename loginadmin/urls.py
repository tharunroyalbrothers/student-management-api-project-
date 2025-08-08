from django.urls import path
from .views import RegisterView, LoginView, LogoutView,UpdateUserView,DeleteUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update/', UpdateUserView.as_view(), name='update-user'),
    path('delete/', DeleteUserView.as_view(),name='delete-user'),
]
