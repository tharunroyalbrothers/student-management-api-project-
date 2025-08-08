from django.urls import path
from .views import (
    StudentCreateView,
    StudentDetailView,
    StudentUpdateView,
    StudentDeleteView,
)


urlpatterns = [
    path('add/', StudentCreateView.as_view(), name='student-add'),
    path('view/<str:usn>/', StudentDetailView.as_view(), name='student-view'),
    path('update/<str:usn>/', StudentUpdateView.as_view(), name='student-update'),
    path('delete/<str:usn>/', StudentDeleteView.as_view(), name='student-delete'),
]
