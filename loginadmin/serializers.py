from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
import re

class RegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        write_only=True,
        required=True,
        allow_blank=False,
        error_messages={
            "blank": "Phone number can't be empty",
            "required": "Phone number is required"
        }
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'phone_number')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True,
                'error_messages': {
                    "blank": "Password can't be empty",
                    "required": "Password can't be empty"
                }
            },
            "email": {"required": True}
        }

    def validate_username(self, username):
        username = ' '.join(username.strip().split())
        if not username:
            raise serializers.ValidationError("UserName can't be empty")
        elif username.isdigit():
            raise serializers.ValidationError("UserName can't be a number")
        elif '..' in username:
            raise serializers.ValidationError("UserName is invalid")
        elif username.endswith('.') or username.startswith('.'):
            raise serializers.ValidationError("UserName is invalid")
        elif not all(char.isalpha() or char.isspace() or char == '.' for char in username):
            raise serializers.ValidationError("UserName is invalid")
        return username

    def validate_password(self, password):
        password = password.strip()
        if password is None:
            raise serializers.ValidationError("Password can't be empty")
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", password):
            raise serializers.ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", password):
            raise serializers.ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", password):
            raise serializers.ValidationError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise serializers.ValidationError("Password must contain at least one special character")
        return password

    def validate_email(self, email):
        email = email.strip().lower()
        if not email:
            raise serializers.ValidationError("Email can't be empty")
        elif User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        elif '..' in email or email.startswith('.') or email.endswith('.') \
            or email.startswith('-') or email.endswith('-') \
            or '--' in email or '.-' in email or '-.' in email \
            or ' ' in email or email.count('@') != 1:
            raise serializers.ValidationError("Invalid Email")
        return email

    def validate_phone_number(self, phone_number):
        phone_number = phone_number.strip()
        if phone_number is None or not phone_number:
            raise serializers.ValidationError("Phone number can't be empty")
        if len(phone_number) != 10:
            raise serializers.ValidationError("Invalid phone number")
        if UserProfile.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError("Phone number already exists")
        return phone_number

    def create(self, validated_data):
        phone_number = validated_data.pop("phone_number")
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"]
        )
        UserProfile.objects.create(user=user, phone_number=phone_number)
        return user



class UpdateUserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        source='profile.phone_number',
        required=False,
        allow_blank=False,
        error_messages={
            "blank": "Phone number can't be empty",
        }
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number']

    def validate_username(self, value):
        username = value.strip()
        if not username:
            raise serializers.ValidationError("Username can't be empty")
        elif username.isdigit():
            raise serializers.ValidationError("Username can't be a number")
        return username

    def validate_email(self, value):
        email = value.strip().lower()
        if not email:
            raise serializers.ValidationError("Email can't be empty")
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise serializers.ValidationError("Email already in use")
        return email

    def validate_phone_number(self, value):
        phone = value.strip()
        user = self.instance
        if not phone:
            raise serializers.ValidationError("Phone number can't be empty")
        if not phone.isdigit() or len(phone) != 10:
            raise serializers.ValidationError("Invalid phone number")
        if UserProfile.objects.exclude(user=user).filter(phone_number=phone).exists():
            raise serializers.ValidationError("Phone number already in use")
        return phone

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile_data = validated_data.get('profile', {})
        phone_number = profile_data.get('phone_number')
        if phone_number:
            instance.profile.phone_number = phone_number
            instance.profile.save()

        return instance

