from rest_framework import generics
from .models import Student
from .serializers import StudentCreateSerializer, StudentUpdateSerializer, StudentBaseSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound,PermissionDenied
from rest_framework.permissions import IsAuthenticated
from loginadmin.authentication import CsrfExemptSessionAuthentication


class StudentCreateView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CsrfExemptSessionAuthentication]

    
    def get(self, request, *args, **kwargs):
        return Response(
            {"message": "Enter the student details"},
            status=status.HTTP_200_OK
        )
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  
        self.perform_create(serializer)

        return Response(
            {
                "message": "Student details created",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

class StudentDetailView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentBaseSerializer
    lookup_field = 'usn'
    authentication_classes = [CsrfExemptSessionAuthentication]

    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"message": "Please login to view student details."}, status=status.HTTP_401_UNAUTHORIZED)

        return super().get(request, *args, **kwargs)

    def get_object(self):
        usn = self.kwargs.get('usn', '').upper()
        try:
            return Student.objects.get(usn__iexact=usn)
        except Student.DoesNotExist:
            raise NotFound(detail="No student found with this USN")

class StudentUpdateView(generics.UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentUpdateSerializer
    lookup_field = 'usn'
    authentication_classes = [CsrfExemptSessionAuthentication]

    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"message": "Please login to update student details."}, status=status.HTTP_401_UNAUTHORIZED)
        student = self.get_object()
        serializer = self.get_serializer(student)
        return Response({
            "message": "Current student details",
            "data": serializer.data
        })
        
    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"message": "Please login to update student details."}, status=status.HTTP_401_UNAUTHORIZED)
        
        if 'usn' in request.data:
            return Response({"error": "USN cannot be updated."}, status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)
    
    def get_object(self):
        usn = self.kwargs.get('usn', '').upper()
        try:
            return Student.objects.get(usn__iexact=usn)
        except Student.DoesNotExist:
            raise NotFound(detail="No student found with this USN")

class StudentDeleteView(generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentBaseSerializer
    lookup_field = 'usn'
    authentication_classes = [CsrfExemptSessionAuthentication]

    

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"message": "Please login to view student details before deletion."}, status=status.HTTP_401_UNAUTHORIZED)

        student = self.get_object()
        serializer = self.get_serializer(student)
        return Response({
            "message": "Student to be deleted",
            "data": serializer.data
        })

    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"message": "Please login to delete student details."}, status=status.HTTP_401_UNAUTHORIZED)
        
        student = self.get_object()
        usn = student.usn
        self.perform_destroy(student)
        return Response(
            {"message": f"Student with USN {usn} has been deleted."},
            status=status.HTTP_200_OK
        )


        return super().delete(request, *args, **kwargs)

    def get_object(self):
        usn = self.kwargs.get('usn', '').upper()
        try:
            return Student.objects.get(usn__iexact=usn)
        except Student.DoesNotExist:
            raise NotFound(detail="No student found with this USN")
