from rest_framework import serializers
from .models import Student
import re

class StudentBaseSerializer(serializers.ModelSerializer):
    course_map={
    "cse":"computer science",
    "cs":"computer science",
    "computer science":"computer science",
    "ise":"information science",
    "it":"information science",
    "information science":"information science",
    "ece":"electronics and communication",
    "ec":"electronics and communication",
    "electronics and communication":"electronics and communication",
    "civil":"civil engineering",
    "cv":"civil engineering",
    "civil engineering":"civil engineering",
    "me":"mechanical engineering",
    "mech":"mechanical engineering",
    "mec":"mechanical engineering", 
    "mechanical engineering":"mechanical engineering",
    "ae":"aeronautical engineering",
    "aero":"aeronautical engineering",
    "aeronautical engineering":"aeronautical engineering",
    "aiml":"artificial intelligence and machine learning",
    "ai":"artificial intelligence and machine learning",
    "artificial intelligence and machine learning":"artificial intelligence and machine learning",
    "csd":"computer science and design",
    "computer science and design":"computer science and design",
}
    usn = serializers.CharField(
        required=True,
        error_messages={
            "blank": "USN can't be empty.",
            "required": "USN is required."
        }
    )
    name = serializers.CharField(
        required=True,
        error_messages={
            "blank": "Name can't be empty.",
            "required": "Name is required."
        }
    )
    email = serializers.EmailField(
        required=True,
        error_messages={
            "blank": "Email can't be empty.",
            "required": "Email is required."
        }
    )
    phone = serializers.CharField(
        required=True,
        error_messages={
            "blank": "Phone number can't be empty.",
            "required": "Phone number is required."
        }
    )
    course = serializers.CharField(
        required=True,
        error_messages={
            "blank": "Course can't be empty.",
            "required": "Course is required."
        }
    )
    age = serializers.IntegerField(
        required=True,
        error_messages={
            "invalid": "Age must be a number.",
            "required": "Age is required."
        }
    )
    class Meta:
        model = Student
        fields = '__all__'


    def validate_usn(self, value):
        value = value.strip().upper()
        if len(value) != 10:
            raise serializers.ValidationError("USN is Invalid.")
        if value[0] != '1' or value[1:3].lower() != 'sj':
            raise serializers.ValidationError("USN is Invalid.")
        if not value[5].isalpha() or not value[6].isalpha():
            raise serializers.ValidationError("USN is Invalid.")
        for pos in [3, 4, 7, 8, 9]:
            if not value[pos].isdigit():
                raise serializers.ValidationError("USN is Invalid.")
        return value

    def validate_phone(self, value):
        if not re.match(r"^\d{10}$", value):
            raise serializers.ValidationError("Phone number is Invalid.")
        
        return value

    def validate_email(self, value):
        email = value.strip()
        if not email:
            raise serializers.ValidationError("Email can't be empty")
        if '..' in email or '--' in email or '.-' in email or '-.' in email:
            raise serializers.ValidationError("Invalid email.")
        if email.startswith(('.', '-')) or email.endswith(('.', '-')):
            raise serializers.ValidationError("Invalid email.")
        if ' ' in email:
            raise serializers.ValidationError("Invalid email.")
        if email.count('@') != 1:
            raise serializers.ValidationError("Invalid email.")
        return email
    
    def validate_name(self, value):
        name = ' '.join(value.strip().split())
        if not name:
            raise serializers.ValidationError("Name can't be empty")
        if name.isdigit():
            raise serializers.ValidationError("Name can't be a number")
        if '..' in name or name.startswith('.') or name.endswith('.'):
            raise serializers.ValidationError("Name is Invalid")
        if not all(char.isalpha() or char.isspace() or char == '.' for char in name):
            raise serializers.ValidationError("Name is Invalid")
        
        name = ' '.join(word.capitalize() for word in name.split())
        return name
    
    def validate_age(self, value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Age must be an integer")
        if value <= 0 or value >= 100:
            raise serializers.ValidationError("Age is not Real")
        return value

    def validate_course(self, value):
        course_input = value.strip().lower()
        if not course_input:
            raise serializers.ValidationError("Course can't be empty")
        if not all(char.isalpha() or char.isspace() for char in course_input):
            raise serializers.ValidationError("Course is Invalid")
        if course_input not in self.course_map:
            raise serializers.ValidationError("Course not recognized.")
        return self.course_map[course_input]
    
    
    def validate(self, attrs):
        usn = attrs.get('usn')
        email = attrs.get('email')
        phone = attrs.get('phone')

        if usn:
            qs = Student.objects.filter(usn__iexact=usn)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({"usn": "student with this USN already exists."})

        if email:
            qs = Student.objects.filter(email__iexact=email)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({"email": "This email is already registered."})

        if phone:
            qs = Student.objects.filter(phone=phone)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError({"phone": "This phone number is already registered."})

        return attrs


class StudentCreateSerializer(StudentBaseSerializer):
    class Meta(StudentBaseSerializer.Meta):
        fields = ['usn','name','age','phone','email','course']
    
class StudentUpdateSerializer(StudentBaseSerializer):
    usn=None        
    class Meta:
        model=Student
        exclude = ['usn'] 